import morfeusz2
import argparse

def dec_fem (noun, case):
    response = morf.generate(noun)
    case_num = check_declination(case)
    len_resp = len(response)
    print(case_num)
    print(response)
    if(len_resp-1 > case_num):
        return response[case_num][0]
    else:
        print("Declination unavailable")
        return 0
        
def check_declination(case):
    number = 0
    if(case == 'gen'):
        number = 1
    elif(case == 'dat' or case == 'loc'):
        number = 2
    elif(case == 'acc'):
        number = 3
    elif(case == 'inst'):
        number = 4
    elif(case == 'voc'):
        number = 5
    return number

if __name__ == '__main__':
    morf = morfeusz2.Morfeusz()
    parser = argparse.ArgumentParser(description = 'Declination of words')
    parser.add_argument('noun', type = str, help = 'Noun to make declination')
    parser.add_argument('case', type = str, help = "Case to declinate")
    args = parser.parse_args()
    print(dec_fem(args.noun, args.case))