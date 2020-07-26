import os
import re
import sys

fasta_dic = {}
transcript_dic = {}

def split_fasta(fasta_file):
    header_line = fasta_file.readline()[:-1]
    body_line = ""
    for line in fasta_file.readlines():
        if line[0] != '>':
            body_line += line[:-1]
        else:
            header_line_out = header_line
            body_line_out = body_line
            header_line = line[:-1]
            body_line = ""
            yield header_line_out,body_line_out
            

def getSeq(seqheader,seqbody):
    seqinfo = re.split(r"[\s]",seqheader[1:],3)
    if len(seqinfo) == 4:
        return seqinfo[0],seqinfo[1],seqinfo[2],seqinfo[3],seqbody
    elif len(seqinfo) == 3:
        return seqinfo[0],seqinfo[1],seqinfo[2],None,seqbody
    else:
        return seqinfo[0],None,seqinfo[1],None,seqbody

def dic_addition(fasta_dic,transcript_dic,seq_name,seq_pep,seq_gene,seq_discrption,seq):
    if seq_name in fasta_dic:
        print('replicate sequence')
    else:
        fasta_dic.update({seq_name:{'seq_pep': seq_pep}})
        fasta_dic[seq_name].update({'seq_gene': seq_gene})
        fasta_dic[seq_name].update({'seq_discrption': seq_discrption})
        fasta_dic[seq_name].update({'seq': seq})
    if seq_gene in transcript_dic:
        if len(fasta_dic[transcript_dic[seq_gene]]['seq']) < len(seq):
            transcript_dic[seq_gene] = seq_name
    else:
        transcript_dic.update({seq_gene: seq_name})
    
def chick_lenth(fasta_dic,num):
    for key in list(fasta_dic.keys()):
        if len(fasta_dic[key]['seq']) < num:
            try:
                if key in transcript_dic[fasta_dic[key]['seq_gene']]:
                    del transcript_dic[fasta_dic[key]['seq_gene']]
            except KeyError:
                pass
            yield key,fasta_dic.pop(key)


def longest_transcript(fasta_dic,transcript_dic):
    for key in transcript_dic:
        yield transcript_dic[key],fasta_dic[transcript_dic[key]]

def output_fasta(iter,fileName):
    def cut_text(text,lenth):
        textArr = re.findall('.{'+str(lenth)+'}', text)
        textArr.append(text[(len(textArr)*lenth):])
        return textArr
    f = open(os.path.join(os.getcwd(),fileName),'w')
    for key,dic in iter:
        f.writelines('>'+key+' '+
                     str(dic['seq_pep'])+' '+
                     dic['seq_gene']+' '+
                     str(dic['seq_discrption'])+'\n')
        for line in cut_text(dic['seq'],60):
            f.writelines(line+'\n')

for string in sys.argv[2:(int(sys.argv[1])+2)]:
    FASTA = string
    FASTA_PATH = os.path.join(os.getcwd(), FASTA)
    fasta = open(FASTA_PATH, 'r')
    for header, body in split_fasta(fasta):
        seq_name, seq_pep, seq_gene, seq_discrption, seq = getSeq(header,body)
        dic_addition(fasta_dic,transcript_dic,seq_name,seq_pep,seq_gene,seq_discrption,seq)
    output_fasta(chick_lenth(fasta_dic,50),'sortfasta_'+FASTA)
    output_fasta(longest_transcript(fasta_dic,transcript_dic),'longtransfilter_'+FASTA)
    fasta.close()
    fasta_dic.clear()
    transcript_dic.clear()

