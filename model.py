import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import BaggingClassifier
from keras import layers
from keras import models

#%%
def load_and_preprocess_data():
    df = pd.read_csv('data/donnees-traitees.csv')
    df = df.drop(columns=['CODE', 'ESPECE', 'GENRE_BOTA'])
    
    train, test = train_test_split(df, test_size=0.2, shuffle=True, random_state=10)
    
    x_train = train.drop(columns=['DEFAUT', 'Unnamed: 0', 'index'])
    x_train = x_train.to_numpy()
    y_train = train['DEFAUT'].to_numpy()
    
    x_test = test.drop(columns=['DEFAUT', 'Unnamed: 0', 'index'])
    x_test = x_test.to_numpy()
    y_test = test['DEFAUT'].to_numpy()
    
    return x_train, y_train, x_test, y_test

#%%
def train_random_forest(x_train, y_train, x_test, y_test):
    rf = RandomForestClassifier()
    rf.fit(x_train, y_train)
    print("Accuracy on test set for Random Forest: %f" % rf.score(x_test, y_test))

#%%
def train_decision_tree(x_train, y_train, x_test, y_test):
    tree = DecisionTreeClassifier(max_depth=3)
    tree.fit(x_train, y_train)
    print("Accuracy on test set for Decision Tree: %f" % tree.score(x_test, y_test))

#%%
def train_multinomial(x_train, y_train, x_test, y_test):
    mnb = MultinomialNB().fit(x_train, y_train)
    print("score on test for Naive Bayes: " + str(mnb.score(x_test, y_test))) #70

#%%
def train_logistic_regression(x_train, y_train, x_test, y_test):
    lr=LogisticRegression(max_iter=1000)
    lr.fit(x_train, y_train)
    print("score on test for Logistic Regression: " + str(lr.score(x_test, y_test))) # 83

#%%
def train_k_neighbors(x_train, y_train, x_test, y_test):
    knn = KNeighborsClassifier(algorithm = 'brute', n_jobs=-1)
    knn.fit(x_train, y_train)
    print("train shape: " + str(x_train.shape))
    print("score on test: " + str(knn.score(x_test, y_test)))   # 84

#%%
def train_linear(x_train, y_train, x_test, y_test):
    svm=LinearSVC(C=0.0001)
    svm.fit(x_train, y_train)
    print("score on test: " + str(svm.score(x_test, y_test)))  # 0.7 ou 0.3

#%%
def train_bagging(x_train, y_train, x_test, y_test):
    # max_samples: maximum size 0.5=50% of each sample taken from the full dataset
    # max_features: maximum of features 1=100% taken here all 10K
    # n_estimators: number of decision trees
    bg=BaggingClassifier(DecisionTreeClassifier(),max_samples=0.5,max_features=1,n_estimators=10)
    bg.fit(x_train, y_train)
    print("score on test: " + str(bg.score(x_test, y_test))) #86

#%%
def train_sequential(x_train, y_train, x_test, y_test):
    model=models.Sequential()
    model.add(layers.Dense(5,activation='relu',input_shape=(24,)))
    model.add(layers.Dense(3,activation='relu'))
    model.add(layers.Dense(1,activation='sigmoid'))
    model.compile(optimizer='rmsprop',loss='binary_crossentropy',metrics=['accuracy'])
    model.fit(x_train,y_train,epochs=10,validation_split = 0.15)
    print("score on test: " + str(model.evaluate(x_test,y_test)[1]))   #0.68

#%%
def main():
    x_train, y_train, x_test, y_test = load_and_preprocess_data()
    
    train_random_forest(x_train, y_train, x_test, y_test)
    train_decision_tree(x_train, y_train, x_test, y_test)
    train_multinomial(x_train, y_train, x_test, y_test)
    train_logistic_regression(x_train, y_train, x_test, y_test)
    train_k_neighbors(x_train, y_train, x_test, y_test)
    train_linear(x_train, y_train, x_test, y_test)
    train_bagging(x_train, y_train, x_test, y_test)
    train_sequential(x_train, y_train, x_test, y_test)

if __name__ == "__main__":
    main()
