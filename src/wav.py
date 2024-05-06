from construct import *
import math
import sys

RiffChunk = Struct(
    "magic" / Const(b"RIFF"),
    "size" / Int32ul,
    "wave" / Const(b"WAVE")
)
FormatSubchunk = Struct(
    "id" / Const(b"fmt "),
    "sub_chunk_size" / Int32ul,
    "audio_format" / Int16ul,
    "num_channels" / Int16ul,
    "sample_rate" / Int32ul,
    "byte_rate" / Int32ul,
    "block_align" / Int16ul,
    "bits_per_sample" / Int16ul
)
DataSubchunk = Struct(
    "id" / Const(b"data"),
    "sub_chunk_size" / Int32ul,
    "data" / GreedyRange(Int16sl)
)
WaveStruct = Struct(
    "riff_chunk" / RiffChunk,
    "format_sub_chunk" / FormatSubchunk,
    "data_sub_chunk" / DataSubchunk
)
def check_extension(bytes):
    magicbytes={'cwk': '0607e100424f424f0607e10000000000000000000001', 'wk1': '0000020006040600080000000000',
     'wk3': '00001a000010040000000000', 'wk4': '00001a000210040000000000', '123': '00001a00051004',
     'qxd': '00004949585052', 'psafe3': '50575333', 'pcap': '4d3cb2a1', 'pcapng': '0a0d0d0a', 'rpm': 'edabeedb',
     'sqlitedb': '53514c69746520666f726d6174203300', 'bin': '53503031', 'wad': '49574144', 'PIC': '00',
     'PDB': '000000000000000000000000000000000000000000000000', 'DBA': '00014244', 'TDA': '00014454',
     'TDF$': '54444624', 'TDEF': '54444546', 'ico': '00000100', 'icns': '69636e73', '3gp': '667479703367',
     'heic': '6674797068656963', 'z': '1fa0', 'lzh': '2d686c352d', 'bac': '4241434b4d494b454449534b', 'idx': '494e4458',
     'plist': '62706c697374', 'bz2': '425a68', 'gif': '474946383761', 'tif': '49492a00', 'cr2': '49492a00100000004352',
     'cin': '802a5fd7', 'nui': '4e555255494d47', 'dpx': '53445058', 'exr': '762f3101', 'bpg': '425047fb',
     'jpg': 'ffd8ffe0', 'jp2': '0000000c6a5020200d0a870a', 'qoi': '716f6966', 'ilbm': '464f524d????????494c424d',
     '8svx': '464f524d????????38535658', 'acbm': '464f524d????????4143424d', 'anbm': '464f524d????????414e424d',
     'anim': '464f524d????????414e494d', 'faxx': '464f524d????????46415858', 'ftxt': '464f524d????????46545854',
     'smus': '464f524d????????534d5553', 'cmus': '464f524d????????434d5553', 'yuvn': '464f524d????????5955564e',
     'iff': '464f524d????????46414e54', 'aiff': '464f524d????????41494646', 'lz': '4c5a4950', 'cpio': '303730373037',
     'exe': '5a4d', 'zip': '504b0304', 'rar': '526172211a070100', 'png': '89504e470d0a1a0a', 'com': 'c9',
     'class': 'cafebabe', 'txt': '0efeff', 'ps': '25215053', 'eps': '252150532d41646f62652d332e3120455053462d332e30',
     'chm': '495453460300000060000000', 'hlp': '3f5f', 'pdf': '255044462d', 'asf': '3026b2758e66cf11a6d900aa0062ce6c',
     'ogg': '4f676753', 'psd': '38425053', 'wav': '52494646????????57415645', 'avi': '52494646????????41564920',
     'mp3': '494433', 'bmp': '424d', 'iso': '4344303031', 'cdi': '4344303031', 'mgw': '6d61696e2e6273',
     'nes': '4e45531a', 'd64': 'a03241a0a0a0', 'g64': '4753522d31353431', 'd81': 'a03344a0a0',
     't64': '433634207461706520696d6167652066696c65', 'crt': '2d2d2d2d2d424547494e2043455254494649434154452d2d2d2d2d',
     'fits': '53494d504c4520203d202020202020202020202020202020202020202054', 'flac': '664c6143', 'mid': '4d546864',
     'doc': '0d444f43', 'dex': '6465780a30333500', 'vmdk': '23204469736b2044657363726970746f', 'crx': '43723234',
     'fh8': '41474433', 'toast': '455202000000', 'dmg': '6b6f6c79', 'xar': '78617221', 'dat': '72656766',
     'tar': '7573746172003030', 'oar': '4f4152??', 'tox': '746f7833', 'MLV': '4d4c5649', '7z': '377abcaf271c',
     'gz': '1f8b', 'xz': 'fd377a585a00', 'lz4': '04224d18', 'cab': '49536328', '??_': '535a4444', 'flif': '464c4946',
     'mkv': '1a45dfa3', 'stg': '4d494c20', 'djvu': '41542654464f524d????????444a56', 'der': '3082',
     'csr': '2d2d2d2d2d424547494e20434552544946494341544520524551554553542d2d2d2d2d',
     'key': '2d2d2d2d2d424547494e205245412050524956415445204b45592d2d2d2d2d',
     'ppk': '50755454592d557365722d4b65792d46696c652d333a', 'pub': '2d2d2d2d2d424547494e2053534832204b45592d2d2d2d2d',
     'dcm': '4449434d', 'woff': '774f4646', 'woff2': '774f4632', 'xml': '3c3f786d6c20', 'wasm': '0061736d',
     'lep': 'cf8401', 'swf': '435753', 'deb': '213c617263683e0a', 'webp': '52494646????????57454250',
     'rtf': '7b5c72746631', 'ts': '47', 'm2p': '000001ba', 'mpg': '000001b3', 'mp4': '667479704d534e56', 'zlib': '7801',
     'lzfse': '62767832', 'orc': '4f5243', 'avro': '4f626a01', 'rc': '53455136', 'rbxl': '3c726f626c6f7821',
     'p25': '65877856', 'pcv': '5555aaaa', 'pbt': '785634', 'ez2': '454d5832', 'ez3': '454d5533', 'luac': '1b4c7561',
     'alias': '626f6f6b000000006d61726b00000000', 'Identifier': '5b5a6f6e655472616e736665725d',
     'eml': '52656365697665643a', 'tde': '20020162a01eab0702000000', 'kdb': '3748030200000000583530394b4559',
     'pgp': '85????03', 'zst': '28b52ffd', 'rs': '5253564b44415441', 'sml': '3a290a', 'srt': '310a3030',
     'vpk': '3412aa55', 'ace': '2a2a4143452a2a', 'arj': '60ea', 'zoo': '5a4f4f', 'pbm': '50340a', 'pgm': '50350a',
     'ppm': '50360a', 'wmf': 'd7cdc69a', 'xcf': '67696d7020786366', 'xpm': '2f2a2058504d202a2f', 'aff': '414646',
     'Ex01': '45564632', 'e01': '455646', 'qcow': '514649', 'ani': '52494646????????41434f4e',
     'cda': '52494646????????43444441', 'qcp': '52494646????????514c434d', 'dcr': '58464952????????4d444746',
     'dir': '52494658????????4d563933', 'flv': '464c56',
     'vdi': '3c3c3c204f7261636c6520564d205669727475616c426f78204469736b20496d616765203e3e3e', 'vhd': '636f6e6563746978',
     'vhdx': '7668647866696c65', 'isz': '49735a21', 'daa': '444141', 'evt': '4c664c65', 'evtx': '456c6646696c65',
     'sdb': '73646266', 'grp': '504d4343', 'icm': '4b434d53', 'pst': '2142444e', 'drc': '445241434f',
     'grib': '47524942', 'blend': '424c454e444552', 'jxl': '0000000c4a584c200d0a870a', 'ttf': '0001000000',
     'otf': '4f54544f', 'wim': '4d5357494d000000d000000000', 'slob': '212d31534c4f421f',
     'voc': '437265617469766520566f6963652046696c651a1a00', 'au': '2e736e64', 'hazelrules': '485a4c5200000018',
     'flp': '464c6864', 'flm': '31304c46', 'mny': '000100004d534953414d204461746162617365',
     'accdb': '000100005374616e6461726420414345204442', 'mdb': '000100005374616e64617264204a6574204442',
     'drw': '01ff02040302', 'dss': '03647373', 'adx': '0300000041505052', 'indd': '0606edf5d81d46e5bd31efe7fe74b71d',
     'mxf': '060e2b34020501010d0102010102', 'skf': '07534b46', 'dtd': '0764743264647464',
     'wallet': '0a166f72672e626974636f696e2e7072', 'nri': '0e4e65726f49534f', 'wks': '0e574b53',
     'sib': '0f534942454c495553', 'dsp': '23204d6963726f736f667420446576656c6f7065722053747564696f',
     'amr': '2321414d52', 'sil': '232153494c4b0a', 'hdr': '6e693100', 'vbe': '23407e5e', 'cdb': '0df01dc0',
     'm3u': '234558544d3355', 'm': '6d646600', 'pak': '4b504b41', 'arc': '1a08', 'pl': 'd04f5053', 'nii': '6e2b3100',
     'hl7': '4d53487c', 'pwrdata': '70777264617461',
     'asc': '2d2d2d2d2d424547494e20504750205055424c4943204b454920424c4f434b2d2d2d2d2d', 'cnt': '3a4261736520',
     'vdr': '52494646????????5644524d', 'trd': '52594646????????54524944', 'shw': '52494646????????73687735',
     'shr': '52494646????????73687235', 'shb': '52494646????????73686235', 'mmm': '52494646????????524d4d50',
     'e57': '4153544d2d453537'}
    l = bytes.hex()
    for key in magicbytes:
        if all(l[i:i + 2] == magicbytes[key][i:i + 2] or magicbytes[key][i:i + 2] == '??' for i in range(0, len(magicbytes[key]), 2)):
            return f'.{key}'


class Encode:
    def __init__(self,source,data):
        self.data = data
        self.source = source
        self.parsed = WaveStruct.parse(source)


    def u16(self,value):
        if value & 0x8000:
            return -((value ^ 0xffff) + 1)
        return value
    def write_byte(self,byte,index):
        for i in range(4):
            data=self.parsed.data_sub_chunk.data
            data[index+i]=self.u16((data[index+i]&0xfffc)| (byte & 3))
            byte>>=2
        return 4
    def encode(self,name):
        offset = 0
        hidden_file_size = len(self.data).to_bytes(4,byteorder='little')
        for b in hidden_file_size:
            offset+=self.write_byte(b,offset)
        for b in self.data:
            offset+=self.write_byte(b,offset)
        with open(f"{name}.wav","wb") as f:
            f.write(WaveStruct.build(self.parsed))

class Decode:
    def __init__(self,data):
        self.data = data
        self.parsed = WaveStruct.parse(data)
    def read_byte(self,offset):
        byte = 0
        shift = 0
        for i in range(4):
            byte|=((self.parsed.data_sub_chunk.data[offset+i]&3)<<shift)
            shift+=2
        return byte,4
    def decode(self,name):
        offset = 0
        size=0
        shift=0
        for i in range(4):
            (byte,inc)=self.read_byte(offset)
            size|=size|(byte<<shift)
            shift+=8
            offset+=inc
        hidden_data=bytearray()
        for i in range(size):
            (byte,inc)=self.read_byte(offset)
            hidden_data.append(byte)
            offset+=inc
        extension= check_extension(hidden_data) or ''
        with open(f"{name}{extension}","wb") as f:
            f.write(hidden_data)
        return f"{name}{extension}"



def get_available_space(file):
    parsed = WaveStruct.parse(file)
    return math.floor(len(parsed.data_sub_chunk.data)/4)

#przykładowe użycie
'''source_file = open("chime_big_ben.wav", "rb").read()
data_file = open("1200px-Sunflower_from_Silesia2-min.jpg", "rb").read()
print(get_available_space(source_file)/1000,'KB available')
e=Encode(source=source_file,data=data_file)
e.encode("encoded")
data=open("encoded.wav","rb").read()
d=Decode(data=data)
d.decode('decoded')'''

if len(sys.argv)>1:
    if sys.argv[1]=='-e' or sys.argv[1]=='--encode':
        source_file = open(sys.argv[2], "rb").read()
        data_file = open(sys.argv[3], "rb").read()
        e=Encode(source=source_file,data=data_file)
        e.encode(sys.argv[4])
    elif sys.argv[1]=='-d' or sys.argv[1]=='--decode':
        data=open(sys.argv[2],"rb").read()
        d=Decode(data=data)
        d.decode(sys.argv[3])
