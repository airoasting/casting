const http=require('http'),fs=require('fs'),path=require('path');
const ROOT="/Users/jaydenkang/Desktop/New Projects/20260624_50가지 스킬";
const TYPES={'.html':'text/html;charset=utf-8','.js':'text/javascript;charset=utf-8','.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.json':'application/json','.woff2':'font/woff2','.woff':'font/woff'};
http.createServer((req,res)=>{
  let p=decodeURIComponent(req.url.split('?')[0]);
  if(p==='/')p='/index.html';
  const fp=path.join(ROOT,p);
  if(!fp.startsWith(ROOT)){res.writeHead(403);return res.end('forbidden');}
  fs.readFile(fp,(e,data)=>{
    if(e){res.writeHead(404);return res.end('not found');}
    res.writeHead(200,{'Content-Type':TYPES[path.extname(fp).toLowerCase()]||'application/octet-stream'});
    res.end(data);
  });
}).listen(4599,()=>console.log('static server on 4599'));
