import pandas as pd
import os
import sys
import itertools

#f = 'deseq_E2F1_dox_data.csv'
#df = pd.read_csv(f, sep='\t')
#df.to_csv(f, sep=',', index=False)
def seperate_reps(df, cmm_cols):
    def remove_sufix(temp, suffix):
        new_cols = [c.split('_')[1] if c != 'name' else c for c in temp.columns ]
        temp.columns = new_cols
        return temp
    df1 = df[[c for c in df.columns if (('rep1' in c) )]]
    df1 = remove_sufix(df1, 'rep1')
    df1 = df1[cmm_cols]
    df2 = df[[c for c in df.columns if (('rep2' in c))]]
    df2 = remove_sufix(df2, 'rep2')
    df2 = df2[cmm_cols]
    avg = (df1+df2)/2
    avg['name'] = df['name']
    avg = avg.set_index('name')
    #print(df1.head())
    #print(df2.head())
    #print(df.head())
    print(avg.head())
    return avg

def read_file(f):
    df = pd.read_csv(f)
    if 'Unnamed: 0' in df:
        df = df.rename(columns={'Unnamed: 0':'name'})
    df['name'] = df['name'].apply(lambda x:x.split('.')[0])
    return df

def get_all_data():
    files = [f for f in os.listdir('.') if 'deseq' in f]
    for f in files:
        df = read_file(f)
        df_ = seperate_reps(df,  ['0hr', '2hr', '6hr' , '12hr'])
        print(df_.transpose().index)
        df_.transpose().iloc[:,:40].to_csv('avg/avg_'+f.split('.')[0]+'.csv', index=False)

def get_data_per_label():
    files = ['29388_2338_kmeans_5c_classes.csv']
    for f in files:
        df = read_file(f)
        labels = set(df['class'].values.tolist())
        labels_info = [{} for l in labels]
        for l in labels:
            dl = df[df['class']==l]
            dl = dl.set_index('name')
            dl = dl.drop('class', axis =1)
            print(dl.transpose().index)
            dl.transpose().to_csv('labeled/%s_'%l+f, index=False)

def get_cmm_genes_bw_conditions():
    files = ['E2F1_all_big_sigs.csv','EV_dox_all_big_sigs.csv','EV_ser_all_big_sigs.csv']
    genes = []
    for f in files:
        df = read_file('significants/'+f)
        genes.append(set(df['name'].values.tolist()))
    data = itertools.combinations([0,1,2], 2)
    subsets = list(data)
    for p in subsets:
            s1 = genes[p[0]]
            s2 = genes[p[1]]
            print(files[p[0]], files[p[1]], len(s1.intersection(s2)))

def test():
    conditions = ['E2F1_dox', 'EV_ser', 'EV_dox']
    for c in conditions:
        dir_ = os.path.join('significants/',c)
        files = [f for f in os.listdir(dir_)]
        for f in files:
            df = pd.read_csv(os.path.join(dir_,f), sep='\t')
            df = df.reset_index()
            #df['index'] = df['index'].apply(lambda x:x.split('.')[0])
            df = df.rename(columns={'index':'name'})
            df.to_csv(os.path.join(dir_,'wdot'+f), sep=',', index=False)
            print(df.head())

def test2():
    dir_ = 'significants/'
    files = [f for f in os.listdir(dir_) if '.csv' in f]
    for f in files:
        file_ = os.path.join(dir_,f)
        print(file_)
        df = pd.read_csv(file_, sep=',')
        #df = df.reset_index()
        #print(df.head())
        #continue
        #df['index'] = df['index'].apply(lambda x:x.split('.')[0])
        df = df.rename(columns={'Unnamed: 0':'name'})
        df['name'] = df['name'].apply(lambda x:x.split('.')[0])
        df.to_csv(os.path.join(dir_,'wdot_'+f), sep=',', index=False)
        print(df.head())
#get_data_per_label()
test2()
sys.exit()
df = read_file('all/t_non_zero.csv')
#df['ID'] = df['ID'].apply(lambda x:x.split('.')[0])
df.to_csv('all/t_non_zero.csv', index=False)
print(df.head())
