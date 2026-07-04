#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为390位三国人物生成古典风格头像。势力色渐变+姓氏字+装饰边框+朱红印章。"""
import os, re, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PERSONS_TS = '/workspace/sanguo-system/src/mock/persons.ts'
OUT_DIR = '/workspace/sanguo-system/public/avatars'
FONT_PATH = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
BOLD_FONT = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'

FACTION = {
    1: {'main':'#22c55e','dark':'#15803d','light':'#86efac','name':'蜀'},
    2: {'main':'#3b82f6','dark':'#1e3a8a','light':'#93c5fd','name':'魏'},
    3: {'main':'#f59e0b','dark':'#92400e','light':'#fcd34d','name':'吴'},
    4: {'main':'#6b7280','dark':'#374151','light':'#9ca3af','name':'雄'},
}
SIZE = 256

def hex2rgb(h):
    h=h.lstrip('#')
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def radial(size, inner, outer):
    img=Image.new('RGB',(size,size),outer)
    px=img.load()
    cx=cy=size/2
    mx=math.sqrt(cx*cx+cy*cy)
    for y in range(size):
        for x in range(size):
            r=math.sqrt((x-cx)**2+(y-cy)**2)/mx
            r=min(1.0,r**1.2)
            px[x,y]=(int(inner[0]*(1-r)+outer[0]*r),int(inner[1]*(1-r)+outer[1]*r),int(inner[2]*(1-r)+outer[2]*r))
    return img

def texture(img, n=12):
    w,h=img.size; op=img.load()
    out=Image.new('RGB',img.size); np=out.load()
    random.seed(42)
    for y in range(h):
        for x in range(w):
            r,g,b=op[x,y]
            d=random.randint(-n,n)
            np[x,y]=(max(0,min(255,r+d)),max(0,min(255,g+d)),max(0,min(255,b+d)))
    return out

def vignette(img):
    w,h=img.size
    v=Image.new('L',(w,h),0)
    d=ImageDraw.Draw(v)
    d.ellipse([-40,-40,w+40,h+40],fill=0)
    v=v.filter(ImageFilter.GaussianBlur(50))
    dark=Image.new('RGBA',(w,h),(0,0,0,0))
    dp=dark.load(); vp=v.load()
    for y in range(h):
        for x in range(w):
            dp[x,y]=(0,0,0,int((vp[x,y]/255.0)*80))
    return Image.alpha_composite(img.convert('RGBA'),dark)

def draw_frame(d, size, cmain, cgold, gold=True):
    if gold:
        d.rectangle([0,0,size-1,size-1],outline=cmain,width=6)
        d.rectangle([8,8,size-9,size-9],outline=cgold,width=2)
    else:
        d.rectangle([0,0,size-1,size-1],outline=cmain,width=4)
    # 四角
    for cx,cy in [(14,14),(size-14,14),(14,size-14),(size-14,size-14)]:
        d.rectangle([cx-5,cy-5,cx+5,cy+5],outline=cgold,width=1)

def draw_seal(d, size, char):
    s=42; m=16
    x0=size-s-m; y0=size-s-m; x1=x0+s; y1=y0+s
    d.rectangle([x0,y0,x1,y1],fill=(168,32,26))
    d.rectangle([x0,y0,x1,y1],outline=(100,10,10),width=2)
    d.rectangle([x0+3,y0+3,x1-3,y1-3],outline=(100,10,10),width=1)
    try: f=ImageFont.truetype(BOLD_FONT,24)
    except: f=ImageFont.load_default()
    b=d.textbbox((0,0),char,font=f)
    tw=b[2]-b[0]; th=b[3]-b[1]
    d.text((x0+(s-tw)/2-b[0],y0+(s-th)/2-b[1]),char,font=f,fill=(255,230,200))

def draw_char(img, char, size, fs, opacity=1.0):
    try: f=ImageFont.truetype(BOLD_FONT,int(fs))
    except: f=ImageFont.load_default()
    cx=cy=size/2
    sh=Image.new('RGBA',img.size,(0,0,0,0)); sd=ImageDraw.Draw(sh)
    b=sd.textbbox((0,0),char,font=f); tw=b[2]-b[0]; th=b[3]-b[1]
    tx=cx-tw/2-b[0]; ty=cy-th/2-b[1]
    sd.text((tx+3,ty+3),char,font=f,fill=(0,0,0,int(140*opacity)))
    img.paste(sh.filter(ImageFilter.GaussianBlur(1.2)),(0,0),sh)
    ov=Image.new('RGBA',img.size,(0,0,0,0)); od=ImageDraw.Draw(ov)
    sc=(40,20,10,int(255*opacity))
    for dx,dy in [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,2),(-2,2),(2,-2)]:
        od.text((tx+dx,ty+dy),char,font=f,fill=sc)
    od.text((tx,ty),char,font=f,fill=(250,245,230,int(255*opacity)))
    img.paste(ov,(0,0),ov)
    return img

def parse():
    with open(PERSONS_TS,'r',encoding='utf-8') as f: c=f.read()
    pat=re.compile(r"\{\s*id:\s*(\d+),\s*name:\s*'([^']*)',.*?factionId:\s*(\d+),.*?importance:\s*(\d+),.*?category:\s*'(main|supporting|minor|unnamed)'",re.DOTALL)
    return [{'id':int(m[1]),'name':m[2],'fid':int(m[3]),'imp':int(m[4]),'cat':m[5]} for m in pat.finditer(c)]

def gen(p, out):
    fc=FACTION.get(p['fid'],FACTION[4])
    cmain=hex2rgb(fc['main']); cdark=hex2rgb(fc['dark']); clight=hex2rgb(fc['light'])
    gold=(212,175,55)
    bg=radial(SIZE,clight,cdark)
    bg=texture(bg,10)
    img=vignette(bg)
    d=ImageDraw.Draw(img)
    with_gold = p['cat'] in ('main','supporting')
    draw_frame(d,SIZE,cmain,gold,with_gold)
    # 顶部势力标
    if p['cat'] in ('main','supporting'):
        try: sf=ImageFont.truetype(FONT_PATH,16)
        except: sf=ImageFont.load_default()
        t=fc['name']; b=d.textbbox((0,0),t,font=sf); tw=b[2]-b[0]; th=b[3]-b[1]
        tx=(SIZE-tw)/2-b[0]; ty=20-b[1]
        d.rectangle([tx-10,ty-3,tx+tw+10,ty+th+3],fill=cdark+(200,),outline=gold,width=1)
        d.text((tx,ty),t,font=sf,fill=(240,215,110))
    # 中央字
    char=p['name'][0] if p['name'] else '?'
    base=SIZE*(0.55 if p['cat']=='main' else 0.5 if p['cat']=='supporting' else 0.45 if p['cat']=='minor' else 0.4)
    extra=(p['imp']-5)*4 if p['imp']>5 else 0
    op=1.0 if p['cat'] in ('main','supporting') else 0.88 if p['cat']=='minor' else 0.75
    img=draw_char(img,char,SIZE,base+extra,op)
    d=ImageDraw.Draw(img)
    if p['cat'] in ('main','supporting'):
        draw_seal(d,SIZE,char)
    img.convert('RGB').save(out,'PNG',optimize=True)

def main():
    os.makedirs(OUT_DIR,exist_ok=True)
    ps=parse()
    print(f'解析 {len(ps)} 人物')
    ok=0
    for i,p in enumerate(ps,1):
        try:
            gen(p,os.path.join(OUT_DIR,f"person_{p['id']}.png")); ok+=1
        except Exception as e:
            print(f'失败 id={p["id"]} {e}')
        if i%100==0: print(f'进度 {i}/{len(ps)}')
    print(f'完成 {ok}/{len(ps)}')

if __name__=='__main__':
    main()
