'''
Function:
	根据中文名字推断性别
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os
import csv
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


'''根据中文名字判断性别'''
class GenderPredictor(QWidget):
	def __init__(self, parent=None, **kwargs):
		super(GenderPredictor, self).__init__(parent)
		# 定义界面
		self.setWindowTitle('姓名猜测性别-公众号: Charles的皮卡丘')
		self.setWindowIcon(QIcon('data/icon.png'))
		self.setFixedSize(400, 200)
		self.name_label = QLabel('中文姓名:')
		self.male_label = QLabel('男生概率:')
		self.female_label = QLabel('女生概率:')
		self.button = QPushButton('预测')
		self.name_edit = QLineEdit()
		self.male_edit = QLineEdit()
		self.female_edit = QLineEdit()
		self.grid = QGridLayout()
		self.grid.setSpacing(12)
		self.grid.addWidget(self.name_label, 0, 0)
		self.grid.addWidget(self.male_label, 1, 0)
		self.grid.addWidget(self.female_label, 2, 0)
		self.grid.addWidget(self.name_edit, 0, 1)
		self.grid.addWidget(self.male_edit, 1, 1)
		self.grid.addWidget(self.female_edit, 2, 1)
		self.grid.addWidget(self.button, 0, 2)
		self.setLayout(self.grid)
		self.button.clicked.connect(lambda: self.predict(self.name_edit.text()))
		# 模型初始化
		self.name_freqs = self.readCSV(os.path.join(os.getcwd(), 'data/freqs.csv'))
		self.male_total = 0
		self.female_total = 0
		for key, value in self.name_freqs.items():
			self.male_total += int(value[0])
			self.female_total += int(value[1])
		self.total = self.male_total + self.female_total
		self.name_probs = {}
		for key, value in self.name_freqs.items():
			self.name_probs[key] = (int(value[0])/self.male_total, int(value[1])/self.female_total)
	'''预测性别'''
	def predict(self, name):
		def genderprob(name, probs, type_='male'):
			assert type_ in ['male', 'female']
			if type_ == 'male':
				p = self.male_total / self.total
				for c in name:
					p *= probs.get(c, (0, 0))[0]
			else:
				p = self.female_total / self.total
				for c in name:
					p *= probs.get(c, (0, 0))[1]
			return p
		for c in name:
			assert u'\u4e00' <= c <= u'\u9fa0'
		male_prob = genderprob(name, self.name_probs, 'male')
		female_prob = genderprob(name, self.name_probs, 'female')
		result = {'male': male_prob / (male_prob + female_prob), 'female': female_prob / (male_prob + female_prob)}
		self.male_edit.setText(str(result['male']))
		self.female_edit.setText(str(result['female']))
		return result
	'''读取数据集'''
	def readCSV(self, csvpath='freqs.csv'):
		fp = open(csvpath, 'r', encoding='utf-8')
		csv_reader = csv.reader(fp)
		name_freqs = {}
		for idx, row in enumerate(csv_reader):
			if idx == 0: continue
			name_freqs[row[0]] = (row[1], row[2])
		return name_freqs


'''run'''
if __name__ == '__main__':
	app = QApplication(sys.argv)
	client = GenderPredictor()
	client.show()
	sys.exit(app.exec_())