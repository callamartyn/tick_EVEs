#!/bin/env bash
$HOME/programs/ncbi-blast-2.9.0+/bin/blastx -query $HOME/EVE/data/I_scapularis/GCA_000208615.1_JCVI_ISG_i3_1.0_genomic.fna \
-db $HOME/db/viral/refseq/viral.1.protein.faa -outfmt '6' -out $HOME/EVE/out/Iscap_blastx_vprot_1e-03.tsv -evalue 1e-03 \
-num_threads $NSLOTS

qstat -j $JOB_ID
