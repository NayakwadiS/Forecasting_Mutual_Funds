
def SMA(df):
    days = 30
    df['nav'] =df['nav'].astype(float)
    pred = []
    for i in range(days):
        value = df['nav'][i:len(df)].sum() + sum(pred)
        pred.append(round(value/len(df),4))
    # print('SMA 30',pred)
    return pred
