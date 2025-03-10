from SFAClassifier import SFAClassifier
from xgboost import DMatrix, train, Booster
import numpy as np

# 导入依赖和继承关系：代码首先从之前定义的 SFAClassifier 类导入必要的依赖，然后通过继承方式扩展为一个新的类 SFARandomForestClassifier。
class SFARandomForestClassifier(SFAClassifier):
    # 构造函数和初始化：在构造函数中，首先调用父类（SFAClassifier）的构造函数，然后设置特定于随机森林的模型名称。这个类扩展了父类的功能，并通过覆盖一些方法来定制化。
    def __init__(self, ds_name, seed):
        super().__init__(ds_name, seed)
        self.model_name = 'random_forest'

    def objective(self, trial):
        pass
    # 超参数和模型训练：get_hyper_params 方法返回了随机森林的超参数配置，train 方法用于初始化并训练随机森林分类器。训练过程中使用了 XGBoost 库的 DMatrix 格式来处理数据。
    def get_hyper_params(self):
        """
        Return the hyperparamters of random forest using the XGBoost implementation
        """
        params = {
                  'verbosity': 0,
                  'objective': self.get_task(),
                  'num_class': 1 if self.get_n_classes() == 2 else self.get_n_classes(),
                  'colsample_bynode': np.sqrt(self.get_n_features()) / self.get_n_features(),
                  'learning_rate': 1,
                  'num_parallel_tree': 250,
                  'subsample': 0.63,
                  'tree_method': 'auto'
        }
        return params

    def train(self, x_train, y_train):
        """
        Initialize random forest classifier and train it
        :param x_train: train features
        :param y_train: train target
        :return: the trained classifier
        """
        params = self.get_hyper_params()
        params['num_class'] = 1 if self.get_n_classes() == 2 else self.get_n_classes()
        dtrain = DMatrix(x_train, label=y_train, enable_categorical=True) if self.categories is not None else DMatrix(x_train, label=y_train)
        return train(params=params, dtrain=dtrain, num_boost_round=1)

    def predict_proba(self, clf, val_data):
        """
        Return the predicted probability for the given classifier.
        :param clf: LGBM classifier
        :param val_data: data
        :return: val_data's predicted probability
        """
        x_val, y_val = val_data[0], val_data[1]
        dvalid = DMatrix(x_val, label=y_val, enable_categorical=True) if self.categories is not None else DMatrix(x_val, label=y_val)
        probs = clf.predict(dvalid)
        if self.get_n_classes() == 2:
            probs = np.array([np.array([1 - i, i]) for i in probs])
        return probs

    def get_task(self):
        """
        Return the task based on the amount of classed in the data
        :return: 'binary:logistic' if there are two classed and 'multi:softprob' otherwise
        """
        return 'binary:logistic' if self.get_n_classes() == 2 else 'multi:softprob'

    @staticmethod
    def save_model(clf, path):
        """
       Saved the model in .model format
       :param clf: random forest classifier
       :param path: path to save the model in
       """
        clf.save_model(path + '.model')

    @staticmethod
    def load_model(path):
        """
        Load the random forest  classifier from the given path
        :param path: path
        :return: random forest  classifier
         """
        bst = Booster()
        bst.load_model(path + '.model')
        return bst

    def get_DMatrix(self, X, y):
        """
        Wrap the dataframe in a DMatrix
        :param X: features
        :param y: target
        :return: data in DMatrix format
        """
        if self.get_categories() is not None:
            return DMatrix(X, label=y, enable_categorical=True)
        else:
            return DMatrix(X, label=y)
