(declare-const rvalue_bufsize (_ BitVec 32))
(declare-const lvalue_bufsize (_ BitVec 32))
(declare-const rreturn (_ BitVec 32))
(declare-const lreturn (_ BitVec 32))
(assert (and (= rreturn rvalue_bufsize) (= lreturn lvalue_bufsize)))