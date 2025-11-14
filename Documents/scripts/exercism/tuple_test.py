combined_record_group=(('Brass Spyglass', '4B', 'Abandoned Lighthouse', ('4', 'B'), 'Blue'), ('Vintage Pirate Hat', '7E', 'Quiet Inlet (Island of Mystery)', ('7', 'E'), 'Orange'), ('Crystal Crab', '6A', 'Old Schooner', ('6', 'A'), 'Purple'))
def main():
    clean_up(combined_record_group)

def clean_up(n):
    clean_list=[]
    for element in combined_record_group:
        clean_list.append(element[:1]+element[2:])
    clean_tuple=(*clean_list,)
    print('\n'.join(map(str, clean_tuple)))

if __name__=="__main__":
    main()
