(declare-const rvalue_col_sep_length (_ BitVec 32))
(declare-const lvalue_col_sep_length (_ BitVec 32))
(declare-const rreturn (_ BitVec 32))
(declare-const lreturn (_ BitVec 32))
(assert (and (= rreturn rvalue_col_sep_length) (= lreturn lvalue_col_sep_length)))