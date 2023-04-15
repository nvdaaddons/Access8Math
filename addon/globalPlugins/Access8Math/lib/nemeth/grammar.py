import csv
import os

from .utils import nemeth2symbol_with_priority


BASE_DIR = os.path.dirname(__file__)
data_folder = os.path.join(BASE_DIR, "data")

data = {}
for item in ["symbol", "letter", "number"]:
	src = os.path.join(BASE_DIR, data_folder, f"{item}.csv")
	nemeth2symbol = nemeth2symbol_with_priority(src)
	data[item] = sorted(nemeth2symbol.keys(), key=lambda i:len(i), reverse=True)

grammar = r"""
	%ignore "⠀"
	start: "\b" exp "\b" -> exp
		| exp -> exp
	exp: i exp* -> exp
	i: s -> exp_interm
		| s "⠘" exp? "⠐" -> exp_sup
		| s "⠰" exp? "⠐" -> exp_sub
		| "⠐" exp? "⠩" exp? "⠻" -> exp_under
		| "⠐" exp? "⠣" exp? "⠻" -> exp_over
		| "⠐" exp? "⠩" exp? "⠣" s "⠻" -> exp_underover
		| s "⠰" s -> exp_sub_simple
		| s "⠘" s -> exp_sup_simple
		| "⠹" exp? ("⠌"|"⠸") exp? "⠼" -> exp_frac
		| "⠜" exp? "⠻" -> exp_sqrt
		| "⠣" exp? "⠜" exp? "⠻" -> exp_root
	s: "⠷" exp? "⠾" -> exp_par
		| "⠈⠷" exp? "⠈⠾" -> exp_par
		| "⠨⠷" exp? "⠨⠾" -> exp_par
		| OPERAND -> operand
		| OTHER -> other
		| _c -> const
	_c: NUMBER
		| EN_UPPERCASE
		| EN_LOWERCASE
		| EN_UPPERCASE_CONTINUE
	OPERAND: /(⠬|⠤|⠈⠡|⠡|⠨⠌|⠨⠅|⠨⠂|⠐⠅)+/
	OTHER: /({symbols})/
	NUMBER: /⠼?({numbers})+/
	EN_UPPERCASE: /(⠠({ens}))+/
	EN_LOWERCASE: /({ens})+/
	EN_UPPERCASE_CONTINUE: /⠠⠠({ens})+(⠠⠄({ens}))?/
	SPACE: /⠀/
""".format(
	ens="|".join(data["letter"]),
	numbers="|".join(data["number"]),
	symbols="|".join(data["symbol"]),
)