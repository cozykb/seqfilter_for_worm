# seqfilter_for_worm
A script for fasta file from wormbase to filter the longest transcript and seq longer than 50(default parameter)
man：
put the scrpit in your document with fasta file, run by the command in shell below.
$python3 seqfilter_for_worm.py INT file_name
INT : file numbers

warning: this script is designing for fasta file from wormbase, you can use the CDS sequence or protein sequence as input. If you try to use it for fasta files from other databases, please make sure your fasta header shows like ">SEQ_NAME PEP_NAME{selectable} GENE_NAME OTHER_{selectable}"

if you find any bugs please contact me from email:386792253@qq.com
