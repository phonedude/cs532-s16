
def load_data(filename):
	data = {}
	with open(filename) as infile:
		for line in infile:
			entry, actual, predicted, cprob = line.split('|')
			data[entry] = {'actual': actual, 'predicted': predicted, 'cprob': float(cprob.strip())}
	return data

def assess(data, categories):
	results = {}
	for category in categories:
		tp, fp, fn = float(0), float(0), float(0)
		for entry, items in data.iteritems():
			if data[entry]['actual'] != category:
				continue
			if not data[entry]['predicted']:
				fn += 1
			elif data[entry]['actual'] == data[entry]['predicted']:
				tp += 1
			elif data[entry]['actual'] != data[entry]['predicted']:
				fp += 1
		prec = tp / (tp + fp)
		recall = tp / (tp + fn)
		f1 = 2 * (prec * recall) / (prec + recall)
		results[category] = {'p': str(prec), 'r': str(recall), 'f1': str(f1)}
	return results

categories = ['game', 'tourney', 'motorcycles', 'event', 'diy']

T_HEAD = """\\begin{table}[h!]
\centering
\\begin{tabular}{| l | l | l | l |}
\hline
Category & Precision & Recall & F-Measure \\\\
\hline
"""

T_TAIL = """\hline
\end{tabular}
\caption{Question 3: Assessments }
\label{tab:assess}
\end{table}
"""

data = load_data('predict_raw')
res = assess(data, categories)
with open('assess', 'w') as outfile:
	outfile.write(T_HEAD)
	for cat, table in res.iteritems():
		outfile.write(' & '.join([cat, table['p'], table['r'], table['f1']]) + ' \\\\\n')
	outfile.write(T_TAIL)
