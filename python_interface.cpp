#include <boost/python.hpp>

#include <llvm/Analysis/Passes.h>
#include <llvm/Analysis/Verifier.h>
#include <llvm/ExecutionEngine/ExecutionEngine.h>
#include <llvm/ExecutionEngine/JIT.h>
#include <llvm/IR/DataLayout.h>
#include <llvm/IR/DerivedTypes.h>
#include <llvm/IR/IRBuilder.h>
#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/Module.h>
#include <llvm/PassManager.h>
#include <llvm/Support/TargetSelect.h>
#include <llvm/Transforms/Scalar.h>

#include "arithmetic.h"

using namespace llvm;

const char* hello() {
  return "Hello, world!";
}

BOOST_PYTHON_MODULE(arithmetic) {
  using boost::noncopyable;
  using namespace boost::python;

  Initialize();

  def("hello", &hello);
  def("evaluate_expression", &EvaluateExpression);
  def("compile", &Compile, return_value_policy<manage_new_object>());
  def("execute", &Execute);

  class_<ExprAST, noncopyable>("ExprAST", no_init);

  class_<NumberExprAST, bases<ExprAST> >("NumberExprAST", init<double>())
      .def(init<double>());

  class_<VariableExprAST, bases<ExprAST> >("VariableExprAST", init<std::string>())
      .def(init<std::string>());

  class_<BinaryExprAST, bases<ExprAST> >("BinaryExprAST", init<char, ExprAST*, ExprAST*>())
      .def(init<char, ExprAST*, ExprAST*>());

  class_<Code, noncopyable>("Code", no_init);
}
