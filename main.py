import os, struct, zlib

W = H = 1024
BG = (12, 22, 36)
PIX = bytearray(BG * (W * H))

FONT = {
'A':'01110/10001/10001/11111/10001/10001/10001','B':'11110/10001/10001/11110/10001/10001/11110','C':'01111/10000/10000/10000/10000/10000/01111','D':'11110/10001/10001/10001/10001/10001/11110','E':'11111/10000/10000/11110/10000/10000/11111','F':'11111/10000/10000/11110/10000/10000/10000','G':'01111/10000/10000/10111/10001/10001/01111','H':'10001/10001/10001/11111/10001/10001/10001','I':'11111/00100/00100/00100/00100/00100/11111','J':'00111/00010/00010/00010/10010/10010/01100','K':'10001/10010/10100/11000/10100/10010/10001','L':'10000/10000/10000/10000/10000/10000/11111','M':'10001/11011/10101/10101/10001/10001/10001','N':'10001/11001/10101/10011/10001/10001/10001','O':'01110/10001/10001/10001/10001/10001/01110','P':'11110/10001/10001/11110/10000/10000/10000','Q':'01110/10001/10001/10001/10101/10010/01101','R':'11110/10001/10001/11110/10100/10010/10001','S':'01111/10000/10000/01110/00001/00001/11110','T':'11111/00100/00100/00100/00100/00100/00100','U':'10001/10001/10001/10001/10001/10001/01110','V':'10001/10001/10001/10001/10001/01010/00100','W':'10001/10001/10001/10101/10101/10101/01010','X':'10001/10001/01010/00100/01010/10001/10001','Y':'10001/10001/01010/00100/00100/00100/00100','Z':'11111/00001/00010/00100/01000/10000/11111',
'0':'01110/10001/10011/10101/11001/10001/01110','1':'00100/01100/00100/00100/00100/00100/01110','2':'01110/10001/00001/00010/00100/01000/11111','3':'11110/00001/00001/01110/00001/00001/11110','4':'00010/00110/01010/10010/11111/00010/00010','5':'11111/10000/10000/11110/00001/00001/11110','6':'01110/10000/10000/11110/10001/10001/01110','7':'11111/00001/00010/00100/01000/01000/01000','8':'01110/10001/10001/01110/10001/10001/01110','9':'01110/10001/10001/01111/00001/00001/01110',
' ':'00000/00000/00000/00000/00000/00000/00000','-':'00000/00000/00000/11111/00000/00000/00000',':':'00000/00100/00100/00000/00100/00100/00000',',':'00000/00000/00000/00000/00100/00100/01000','.':'00000/00000/00000/00000/00000/00100/00100','’':'00100/00100/00000/00000/00000/00000/00000','/':'00001/00010/00010/00100/01000/01000/10000','&':'01100/10010/10100/01000/10101/10010/01101'
}

def rect(x, y, w, h, color):
    x0, y0, x1, y1 = max(0,x), max(0,y), min(W,x+w), min(H,y+h)
    if x0 >= x1 or y0 >= y1: return
    row = bytes(color) * (x1-x0)
    for yy in range(y0,y1):
        i = (yy*W+x0)*3
        PIX[i:i+len(row)] = row

def text(s, x, y, scale, color, gap=1):
    cx=x
    for ch in s.upper():
        grid=FONT.get(ch,FONT[' ']).split('/')
        for yy,row in enumerate(grid):
            for xx,on in enumerate(row):
                if on=='1': rect(cx+xx*scale,y+yy*scale,scale,scale,color)
        cx += 6*scale + gap
    return cx-x

def line(x1,y1,x2,y2,width,color):
    # deterministic integer line
    dx=abs(x2-x1); sx=1 if x1<x2 else -1; dy=-abs(y2-y1); sy=1 if y1<y2 else -1; err=dx+dy
    while True:
        rect(x1-width//2,y1-width//2,width,width,color)
        if x1==x2 and y1==y2: break
        e=2*err
        if e>=dy: err+=dy; x1+=sx
        if e<=dx: err+=dx; y1+=sy

def panel(x,y,w,h,tag,headline,lines,accent,kind):
    rect(x,y,w,h,(26,42,61)); rect(x,y,w,5,accent)
    text(tag,x+18,y+17,2,(145,169,184))
    text(headline,x+18,y+47,2,(244,247,240),0)
    for n,line_text in enumerate(lines):
        text(line_text,x+18,y+82+n*25,2,(209,220,224),0)
    # Each panel has a small, clean geometric symbol tied to its subject.
    ix=x+w-102; iy=y+76
    if kind=='apec':
        rect(ix,iy,78,47,(31,100,113)); rect(ix+8,iy+8,62,31,(237,183,73)); rect(ix+31,iy+8,16,31,(204,54,54))
        rect(ix+10,iy+51,60,5,(118,198,182))
    elif kind=='gaza':
        rect(ix+5,iy+8,20,35,(167,112,87)); rect(ix+29,iy,18,43,(116,94,82)); rect(ix+51,iy+13,22,30,(145,105,81))
        rect(ix,iy+43,80,6,(203,153,111)); rect(ix+12,iy+52,56,3,(216,182,143))
    elif kind=='iran':
        rect(ix+7,iy+13,65,20,(82,117,136)); rect(ix+18,iy+8,20,29,(188,205,199)); rect(ix+26,iy+2,5,11,(235,183,73))
        line(ix+13,iy+49,ix+66,iy+49,3,(237,112,81)); line(ix+22,iy+42,ix+22,iy+55,3,(237,112,81))
    elif kind=='climate':
        rect(ix+5,iy+23,22,18,(48,143,161)); rect(ix+31,iy+30,23,16,(40,127,155)); rect(ix+58,iy+19,19,25,(54,151,163))
        line(ix+40,iy+21,ix+40,iy+2,4,(126,204,139)); line(ix+40,iy+11,ix+29,iy+5,4,(126,204,139)); line(ix+40,iy+10,ix+51,iy+4,4,(126,204,139))
    elif kind=='water':
        rect(ix+24,iy+3,32,34,(63,172,197)); rect(ix+24,iy+30,32,7,(26,42,61))
        line(ix+40,iy+38,ix+40,iy+50,3,(111,199,219)); line(ix+27,iy+49,ix+53,iy+49,3,(111,199,219))
        rect(ix+7,iy+13,10,5,(226,177,72)); rect(ix+63,iy+22,10,5,(226,177,72))
    elif kind=='asean':
        rect(ix+8,iy+5,62,43,(69,124,148)); rect(ix+14,iy+11,50,31,(26,42,61))
        for dx in (24,36,48): rect(ix+dx,iy+20,7,12,(230,180,73))
        rect(ix+16,iy+49,46,4,(118,198,182))

def png_chunk(kind,data):
    body=kind+data
    return struct.pack('>I',len(data))+body+struct.pack('>I',zlib.crc32(body)&0xffffffff)

def save(path):
    raw=bytearray()
    stride=W*3
    for y in range(H): raw.append(0); raw.extend(PIX[y*stride:(y+1)*stride])
    ihdr=struct.pack('>IIBBBBB',W,H,8,2,0,0,0)
    out=b'\x89PNG\r\n\x1a\n'+png_chunk(b'IHDR',ihdr)+png_chunk(b'IDAT',zlib.compress(bytes(raw),9))+png_chunk(b'IEND',b'')
    with open(path,'wb') as f: f.write(out)

INK=(244,247,240); MUTED=(155,178,190); TEAL=(69,190,177)
text('WEDNESDAY',32,27,2,TEAL,0)
text('18 NOVEMBER 2026',32,55,4,INK,0)
text('THE WORLD IN SIX STORIES',34,94,1,MUTED,0)
rect(32,119,960,2,(67,89,105))
cards=[
 ('EAST ASIA / DIPLOMACY','XI PITCHES OPEN TRADE',('TRUMP ARRIVES FOR APEC','IN SHENZHEN.'),(67,190,177),'apec'),
 ('GAZA / CONFLICT','ISRAEL OPENS CENTRAL GAZA OP',('PALESTINIANS FLEE AS','ISRAELI FORCES MOVE IN.'),(220,125,97),'gaza'),
 ('GULF / CONFLICT','GULF FIGHTING WIDENS',('AP: IRAN ATTACKS KUWAIT','AND BAHRAIN AFTER QESHM.'),(235,112,81),'iran'),
 ('CLIMATE / COP31','ISLANDS DEMAND ACTION',('SMALL ISLAND STATES PRESS','FOR STRONGER CLIMATE STEPS.'),(110,197,145),'climate'),
 ('THAILAND / ENVIRONMENT','ARSENIC POLLUTES RIVERS',('THAILAND SCRAMBLES FOR','CLEAN WATER NEAR MYANMAR.'),(102,191,213),'water'),
 ('SOUTHEAST ASIA / ASEAN','MYANMAR CRITICIZES ASEAN',('MILITARY-BACKED LEADER','SAYS TIES MAY BE REVIEWED.'),(228,179,83),'asean'),
]
cw,ch,gap=470,244,18
for i,(tag,head,body,accent,kind) in enumerate(cards):
    col=i%2; row=i//2
    panel(32+col*(cw+gap),137+row*(ch+15),cw,ch,tag,head,body,accent,kind)
rect(32,920,960,2,(67,89,105))
text('WORLD NEWS  /  WED 18 NOV 2026',32,938,1,MUTED,0)
text('AP • AL JAZEERA • COP31',684,938,1,MUTED,0)
outdir=os.environ.get('MAKEFUN_OUTPUT_DIR','/output')
os.makedirs(outdir,exist_ok=True)
save(os.path.join(outdir,'entry.png'))
