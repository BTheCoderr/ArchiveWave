import { NextRequest, NextResponse } from "next/server";
import { lookup } from "node:dns/promises";
import { isIP } from "node:net";
import { Agent, request } from "undici";
export const runtime = "nodejs";
export const dynamic = "force-dynamic";
const MAX_BYTES = 5_000_000;
const MAX_HOPS = 3;
function publicIPv4(ip:string) {
  if(isIP(ip)!==4)return false;
  const [a,b,c]=ip.split(".").map(Number);
  return !(a===0||a===10||a===127||a>=224||a===169&&b===254||a===172&&b>=16&&b<=31||a===192&&(b===168||b===0||b===88&&c===99)||a===100&&b>=64&&b<=127||a===198&&(b===18||b===19)||a===192&&b===0&&c===0||a===192&&b===0&&c===2||a===198&&b===51&&c===100||a===203&&b===0&&c===113);
}
function checkURL(raw:string) {
  const url=new URL(raw);
  if(!["https:","http:"].includes(url.protocol)||url.username||url.password||url.port&&url.port!==(url.protocol==="https:"?"443":"80"))throw Error("Only public HTTP(S) RSS URLs on standard ports are supported.");
  if(isIP(url.hostname)||url.hostname==="localhost"||!url.hostname.includes(".")||/\.(local|internal|localhost|onion|test|invalid)$/i.test(url.hostname))throw Error("Private or unsupported host.");
  return url;
}
async function fetchRSS(initial:string) {
  let url=checkURL(initial);
  for(let hop=0;hop<=MAX_HOPS;hop++){
    const addresses=await lookup(url.hostname,{all:true,verbatim:true});
    if(!addresses.length||addresses.some(a=>!publicIPv4(a.address)))throw Error("Host resolves to a private or unsupported address.");
    const pinned=addresses.find(a=>a.family===4);
    if(!pinned)throw Error("Only public IPv4 RSS hosts are currently supported.");
    const dispatcher=new Agent({connect:{timeout:5000,lookup:(_host,_opts,callback)=>callback(null,pinned.address,4)}});
    try {
      const response=await request(url.toString(),{dispatcher,maxRedirections:0,headers:{"user-agent":"ArchiveWaveBeta/0.4 (+public RSS metadata audit)","accept":"application/rss+xml, application/xml, text/xml, */*"},headersTimeout:8000,bodyTimeout:8000});
      if([301,302,303,307,308].includes(response.statusCode)){
        const location=response.headers.location;
        await response.body.dump();
        if(!location||hop===MAX_HOPS)throw Error("Too many redirects.");
        url=checkURL(new URL(String(location),url).toString());
        continue;
      }
      if(response.statusCode!==200){await response.body.dump();throw Error("RSS host returned HTTP "+response.statusCode);}
      const length=Number(response.headers["content-length"]||0);
      if(length>MAX_BYTES)throw Error("RSS feed is too large.");
      let total=0;const chunks:Buffer[]=[];
      for await(const chunk of response.body){const b=Buffer.from(chunk);total+=b.length;if(total>MAX_BYTES)throw Error("RSS feed exceeds 5 MB.");chunks.push(b);}
      return Buffer.concat(chunks).toString("utf8");
    }finally{await dispatcher.close();}
  }
  throw Error("Redirect limit reached.");
}
export async function POST(req:NextRequest){
  try{
    const body=await req.json();
    if(typeof body.url!=="string"||body.url.length>2048) return NextResponse.json({error:"Provide a valid RSS URL."},{status:400});
    const xml=await fetchRSS(body.url.trim());
    if(!/<(?:rss|feed)(?:\s|>)/i.test(xml.slice(0,2000)))throw Error("This URL does not appear to contain an RSS or Atom feed.");
    return NextResponse.json({xml},{headers:{"cache-control":"no-store"}});
  }catch(e){return NextResponse.json({error:e instanceof Error?e.message:"RSS fetch failed"},{status:400});}
}
