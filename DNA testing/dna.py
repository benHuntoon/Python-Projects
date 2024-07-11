#Coded by Benjamin Huntoon and Sha'Niece Twitty

#here the global constants are set to use or change when running the program
MASSES          = [135.128, 111.103, 151.128, 125.107]
NUM_NUCLEOTIDES =  4   # number of nucleotides (A,C,G,T)
CODON_LENGTH    =  3   # number of nucleotides per codon
MINIMUM_LENGTH  =  5   # shortest length for valid protein
CG_PERCENTAGE   = 30   # min % C/G for a valid protein

def main():
    #here we print introduction information
    print("This program reports information about DNA")
    print("nucleotide sequences that may encode proteins.")
    #here the user is prompted to input a file to provide data and another to write on
    in_file = open(input("Input file name? "))
    out_file = open(input("Output file name? "),'w')
    lines = in_file.readlines()
    #this for loop runs the program for every different protein in the original file
    for i in range(0, len(lines),2):
        name = lines[i]
        seq_name = lines[i+1]
        junk_count,sequence = find_junk(lines[i+1])
        codons_list = get_codons(sequence)
        chain = nuc_index(sequence)
        counts = get_counts(chain)
        total_mass,mass_list = get_total_mass(counts, junk_count)
        percentages = get_percentages(mass_list, total_mass)
        test = is_protein(codons_list, percentages)
        report_results(name, seq_name, counts, total_mass, percentages, codons_list, test, out_file)

#this function uses returned data from other functions to write the end file
def report_results(name, seq_name, counts, total_mass, percentages, codons_list, test, out_file):
    out_file.write('Region Name: ' + name)
    out_file.write('Nucleotides: ' + seq_name)
    out_file.write('Nuc. Counts: ' + str(counts))
    out_file.write('\n')
    out_file.write('Total Mass%: ' + str(percentages))
    out_file.write('\n')
    out_file.write('Codons List: ' + str(codons_list))
    out_file.write('\n')
    out_file.write('Is Protein?: ' + test)
    out_file.write('\n')
    out_file.write('\n')

def is_protein(codons_list, percentages):
    #this measures the total percentage of mass used by C and G nucleotides
    gc_count = percentages[1] + percentages[2]
    #this checks for the correct starting codon
    if codons_list[0] == 'ATG':
        #this checks for any of the correct ending codons
        if codons_list[-1] == 'TAA' or 'TAG' or 'TGA':
            #this checks if the CG total is greater then the minimum amount
            if round(gc_count,1) >= CG_PERCENTAGE:
                #this checks if the protein is the minimum acceptable length and then returns the correct protein status
                if len(codons_list) >= MINIMUM_LENGTH:
                    return 'YES'
                else:
                    return 'NO'
            else:
                return 'NO'
        else:
            return 'NO'
    else:
        return 'NO'

def get_percentages(mass_list, total_mass):
    #this sets an empty list for nucleotide composition in a protein
    percentages = []
    #this loop determines and appends each nucleotide's composition within a protein and returns the list of percentages
    for items in mass_list:
        mass_perc = (items / total_mass) * 100
        percentages.append(round(mass_perc,1))
    return percentages

def get_total_mass(counts, junk_count):
    #this sets an empty list to add each individual mass to
    mass_list = []
    #this calculates the total mass of junk nucleotides
    junk_mass = junk_count * 100
    total_mass = junk_mass
    #this compares the counted totals of each nucleotide to their respective masses
    #then appending that mass to the list of masses
    for count in range(len(counts)):
        mass = counts[count] * MASSES[count]
        mass_list.append(round(mass,1))
        total_mass += mass
    total_mass = round(total_mass,1)
    #this returns the combined total mass and the list of masses back to main
    return total_mass,mass_list

def nuc_index(sequence):
    chain = sequence.upper()
    #this creates a temporary dictionary to create an index for each
    #nucleotide by tallying each occurence and then returning the dictionary
    tallies = dict()
    for letter in chain:
        if letter in tallies:
            tallies[letter] += 1
        else:
            tallies[letter] = 1
    return tallies
        
def get_counts(chain):
    #this creates an empty list to later translate the dictionary count to
    counts = [0] * NUM_NUCLEOTIDES
    pos = 0
    #this iterates through the dictionary and adds the values of each nucleotide count
    #into the list of counts
    for letters in 'ACGT':
        try:
            counts[pos] = chain[letters]
        #this error raise is used to make a nucleotide count 0 when
        #the nucleotide was not present in the protein
        except KeyError:
            counts[pos] = 0
        pos += 1
    #this returns the list of counts back to main
    return counts
        
    
def get_codons(sequence):
    #this creates a new list for each protein's codons
    codons_list = []
    chain = sequence.upper()
    #this separates the protein in nuc groups of three and then appends those codons
    #to those lists
    while chain:
        codons_list.append(chain[:CODON_LENGTH])
        chain = chain[CODON_LENGTH:]
    #this returns the list of codons
    return codons_list[:-1]

def find_junk(nucs):
    junk = 0
    #this takes a protens codons and removes all junk nucleotides and returns the new
    #protein and the total count of junk necleotides
    nuc_chain = list(nucs)
    for letter in nuc_chain[0:]:
        if letter == '-':
            nuc_chain.remove(letter)
            junk += 1
    result = "".join(nuc_chain)
    return junk, result


main ()
