import re
def to_rna(dna_strand):
    if dna_strand =="":
        return ""
    dna_strand= dna_strand.upper()
    
    map = str.maketrans("GCAT", "CGUA")
    rna = dna_strand.translate(map)
    return rna