import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    # print(F"---people= {people}")

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    # print(f"---probabilities= {probabilities}")

    # Loop over all sets of people who might have the trait
    names = set(people)
    # print(f"---names= {names}")
    # print(f"---powerset= {powerset(names)}")
    for have_trait in powerset(names):
        
        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            # print(f"{have_trait} fails evidence")
            continue
        
        # test condition!
        # if have_trait != {'James'}:
            # continue

        print(f"\nXXX START have_trait= {have_trait}")
        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):

            # test condition!
            # if one_gene != {'Harry'}:
                # continue

            print(f"---onegene= {one_gene}")
            for two_genes in powerset(names - one_gene):

                # test condition!
                # if two_genes != {'James'}:
                    # continue

                print(f"---two_genes= {two_genes}")

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

                # break

            # break
        print(f"\n---END HAVE_GENE LOOP\n")
        
        # break
        
    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
            
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # print(f"---people= {people}")
    # print(f"+++ IN JOINT_PROB FN")
    
    # print(f"---one_gene set = {one_gene}")
    # print(f"---two_gene set = {two_genes}")
    # print(f"---have_trait set = {have_trait}")

    totalprob = 1
    # loop through people 
    # get prob for person gene count 
    for person in people:
        # print(f"+++THIS PERSON = {person}")
        # get parent state for person
        mother = people[person]['mother']
        # print(f"---{person}'s mother= {people[person]['mother']}")
        father = people[person]['father']
        # print(f"---{person}'s father= {people[person]['father']}")
        # do we know how many genes mother has? 
        if mother != None:
            if mother in one_gene:
                mothergenes = 1
                motherprob = .5
            elif mother in two_genes:
                mothergenes = 2
                motherprob = .99
            else:
                mothergenes = 0
                motherprob = 0.01
            # print(f"---mother has {mothergenes} genes")
            # print(f"---motherprob= {motherprob}")
        # do we know how many genes father has? 
        if father != None:
            if father in one_gene:
                fathergenes = 1
                fatherprob = .5
            elif father in two_genes:
                fathergenes = 2
                fatherprob = .99
            else:
                fathergenes = 0
                fatherprob = 0.01
            # print(f"---father has {fathergenes} genes")
            # print(f"---fatherprob= {fatherprob}")
        
        # is person in 1 gene? 
        if person in one_gene:
            # print(f"---{person} is in one_gene set")
            # whats the prob of this person having 1 gene?
            # if no parents - use uncond prob 1 gene 0.03
            if mother == None and father == None:
                geneprob = 0.03
            # elif mother == None:
            #     motherprob = 0.03
            # elif father == None:
            #     fatherprob = 0.03
            else:
                # if parents
                """
                                        fromD * not fromM =          +  not fromD * fromM             1 gene prob   n/w
                if dad = 2, mum = 2    ( .99  *  .01 )  =  .0099    +    ( .01  *  .99 )  = .0099 == .0198          1/9
                if dad = 2, mum = 1    ( .99  *  .5  )  =  .495     +    ( .01  *  .5  )  = .005  == .05            2/9 *2 
                if dad = 2, mum = 0    ( .99  *  .99 )  =  .9801    +    ( .01  *  .01 )  = .0001 == .9802          2/9 *2
                if dad = 1, mum = 2    ( .5   *  .01 )  =  .005     +    ( .5   *  .99 )  = .495  == .05            2/9 *2
                if dad = 1, mum = 1    ( .5   *  .5  )  =  .25      +    ( .5   *  .5  )  = .25   == .5             1/9
                if dad = 1, mum = 0    ( .5   *  .99 )  =  .495     +    ( .5   *  .01 )  = .005  == .5             2/9 *2
                if dad = 0, mum = 2    ( .01  *  .01 )  =  .0001    +    ( .99  *  .99 )  = .9801 == .9802          2/9 *2
                if dad = 0, mum = 1    ( .01  *  .5  )  =  .005     +    ( .99  *  .5  )  = .495  == .5             2/9 *2
                if dad = 0, mum = 0    ( .01  *  .99 )  =  .0099    +    ( .99  *  .01 )  = .0099 == .0198          2/9 *2
                """

                # print(f"---({fatherprob} * {1-motherprob}) + ({1-fatherprob} * {motherprob})")
                geneprob = round(round((fatherprob * round(1-motherprob,6)),6) + round((round(1-fatherprob,6) * motherprob), 6),6)
                # print(f"---{person}'s onegeneprob= {geneprob}")
            traitprob = .56
            # print(f"---{person}'s 1gene traitprob = {traitprob}")
        # is person in 2 gene? 
        elif person in two_genes:
            # print(f"---{person} is in two_gene set")
            # whats the prob of them having 2 genes? 
            """
                                        fromD   *   fromM     2 gene prob
                if dad = 2, mum = 2      .99        .99   =  .9801 
                if dad = 2, mum = 1      .99        .5    =  .495 
                if dad = 2, mum = 0      .99        .01   =  .0099 
                if dad = 1, mum = 2      .5         .99   =  .495 
                if dad = 1, mum = 1      .5         .5    =  .25 
                if dad = 1, mum = 0      .5         .01   =  .005 
                if dad = 0, mum = 2      .01        .99   =  .0099 
                if dad = 0, mum = 1      .01        .5    =  .005 
                if dad = 0, mum = 0      .01        .01   =  .0001 
             """
            # give uncond prob if mum or dad  are unknown
            if mother == None and father == None:
                geneprob = 0.01
            # elif mother == None:
            #     motherprob = 0.01
            # elif father == None:
            #     fatherprob = 0.01
            else:
                geneprob = round( fatherprob * motherprob,6)
                # print(f"---{person}'s twogeneprob= {geneprob}")
            traitprob = .65
            # print(f"---{person}'s 2gene traitprob = {traitprob}")

        # else person has 0 genes 
        else:
            # print(f"---{person} is in zero gene set")
            """ 
                                   not fromD   *  not fromM     2 gene prob
                if dad = 2, mum = 2      .01   *   .01   =  .0001
                if dad = 2, mum = 1      .01   *   .5    =  .005 
                if dad = 2, mum = 0      .01   *   .99   =  .0099 
                if dad = 1, mum = 2      .5    *   .01   =  .005 
                if dad = 1, mum = 1      .5    *   .5    =  .25
                if dad = 1, mum = 0      .5    *   .99   =  .495 
                if dad = 0, mum = 2      .99   *   .01   =  .0099 
                if dad = 0, mum = 1      .99   *   .5    =  .495 
                if dad = 0, mum = 0      .99   *   .99   =  .9801
             """
            # give uncond prob if mum or dad  are unknown
            if mother == None and father == None:
                geneprob = 0.96
                # print(f"---{person} gets unconditional 0gene prob {geneprob}")
            # elif mother == None:
            #     motherprob = 0.96
            # elif father == None:
            #     fatherprob = 0.96
            else:
                geneprob = round(round(1-fatherprob, 6) * round(1-motherprob,6) ,6)
                # print(f"---{person}'s zerogeneprob= {geneprob}")
            traitprob = .01
        # lastly do they have the trait? work out prob for that situation 
        if person not in have_trait:
            # print(f"---{person} not in havetrait")
            traitprob = round(1-traitprob, 6)
            # print(f"---{person}'s not-trait prob = {traitprob}")
        personprob = round(geneprob * traitprob, 6 )
        # print(f"---{person}'s total prob  = {geneprob}*{traitprob} = {personprob}")
        totalprob *= personprob
        # print(f"---multiplied probs of people = {totalprob}")
       
        

        # multiply prob of N gene X prob Trait = persons prob for this state 
        # l0op to next person 
       
    # multiply all peoples probs 
    print(f"---prob of this situation= {totalprob}")
    return totalprob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # print(f"^^^IN UPDATE FN")
    # print(f"---probabilities= {probabilities}")
  
    for person in probabilities:
        # if person in one_gene
        # print(f"---this person= {person}")
        if person in one_gene:
            probabilities[person]['gene'][1] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p
        else:
            probabilities[person]['gene'][0] += p
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p
        
        # if person in two_gene

        # if person in one_gene

        # if person in one_gene


    

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        A = probabilities[person]['gene'][2]
        B = probabilities[person]['gene'][1]
        C = probabilities[person]['gene'][0]
        sumg = A+B+C
        A2 = A/sumg
        B2 = B/sumg
        C2 = C/sumg
        probabilities[person]['gene'][2] = A2
        probabilities[person]['gene'][1] = B2
        probabilities[person]['gene'][0] = C2

        T = probabilities[person]['trait'][True]
        F = probabilities[person]['trait'][False]
        sumt = T + F
        T2 = T/sumt
        F2 = F/sumt
        probabilities[person]['trait'][True] = T2
        probabilities[person]['trait'][False] = F2


        



if __name__ == "__main__":
    main()
