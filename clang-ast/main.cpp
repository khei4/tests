#include "clang/AST/ASTContext.h"
#include "clang/ASTMatchers/ASTMatchFinder.h"
#include "clang/ASTMatchers/ASTMatchers.h"
#include "clang/Frontend/FrontendActions.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Refactoring.h"
#include <clang/ASTMatchers/ASTMatchers.h>
#include <clang/Frontend/TextDiagnosticPrinter.h>
#include <clang/Rewrite/Core/Rewriter.h>
#include <clang/Tooling/Transformer/RangeSelector.h>
#include <clang/Tooling/Transformer/RewriteRule.h>
#include <clang/Tooling/Transformer/Stencil.h>
#include <llvm/Support/CommandLine.h>

#include <cassert>
#include <memory>
using namespace std;
using namespace clang;
using namespace clang::ast_matchers;
using namespace clang::tooling;
using namespace clang::transformer;
using namespace clang::transformer::detail;
using namespace llvm;

// const clang::transformer::RewriteRule makeLoop1024Rule() {
//   auto incLoopMatcher =
//       forStmt(hasLoopInit(declStmt(hasSingleDecl(
//                   varDecl(hasInitializer(integerLiteral(equals(0))))
//                       .bind("initVarName")))),
//               hasIncrement(unaryOperator(
//                   hasOperatorName("++"),
//                   hasUnaryOperand(declRefExpr(
//                       to(varDecl(hasType(isInteger())).bind("incVarName")))))),
//               hasCondition(binaryOperator(
//                   hasOperatorName("<"),
//                   hasLHS(ignoringParenImpCasts(declRefExpr(
//                       to(varDecl(hasType(isInteger())).bind("condVarName"))))),
//                   hasRHS(expr(hasType(isInteger()))))))
//           .bind("forLoop");
//   return applyFirst(
//       {makeRule(incLoopMatcher, changeTo(cat("TODO: rubbed loop")))});
// }

// const auto LoopZeroInitMatcher = hasLoopInit(declStmt(hasSingleDecl(
//     varDecl(hasInitializer(integerLiteral(equals(0)))).bind("initVarName"))));

// const auto LoopIncMatcher = hasIncrement(
//     unaryOperator(hasOperatorName("++"),
//                   hasUnaryOperand(declRefExpr(
//                       to(varDecl(hasType(isInteger())).bind("incVarName"))))));
// const auto IntLoopLTCompMatcher = hasCondition(
//     binaryOperator(hasOperatorName("<"),
//                    hasLHS(ignoringParenImpCasts(declRefExpr(
//                        to(varDecl(hasType(isInteger())).bind("condVarName"))))),
//                    hasRHS(expr(hasType(isInteger())))));

// auto forLoopConditionMatcher =
//     binaryOperator(
//         hasOperatorName("<"),
//         hasParent(forStmt(hasCondition(expr().bind("forCondition")))))
//         .bind("forCondition");

// const StatementMatcher IncLoopMatcher =
//     forStmt(LoopZeroInitMatcher, LoopIncMatcher, IntLoopLTCompMatcher,
//             hasBody(stmt(isExpansionInMainFile()).bind("body")))
//         .bind("forLoop");
// const RewriteRule IncLoopTo1024LoopRule =
//     makeRule(IncLoopMatcher,
//              changeTo(cat("for (int ", name("initVarName"), " = 0;",
//                           name("initVarName"), " < 1024;",
//                           name("initVarName"),
//                           "++)", " {", node("body"), "} ")));

// // handle For
// // FIXME: this is only for Inc Matcher, how ? step also shuold be changed?
// const StatementMatcher UnnestedLoopMatcher =
//     forStmt(LoopZeroInitMatcher, LoopIncMatcher, IntLoopLTCompMatcher,
//             hasBody(stmt(allOf(unless(anyOf(forStmt(), whileStmt(),
//             doStmt())),
//                                isExpansionInMainFile()))
//                         .bind("body")));

// // TODO: handle compound statement nicely.
// const RewriteRule UnnestedLoopTo1024LoopRule =
//     makeRule(UnnestedLoopMatcher,
//              changeTo(cat("for (int ", name("initVarName"), " = 0;",
//                           name("initVarName"), " < 1024;",
//                           name("initVarName"),
//                           "++)", " {", statement("body"), ";} ")));

// // TODO: match against all decl and insert alignas
// const DeclarationMatcher VarDeclExceptLoopConditionMatcher =
//     varDecl(unless(hasAncestor(forStmt())), unless(hasAncestor(whileStmt())),
//             unless(hasAncestor(doStmt())))
//         .bind("varDeclExceptLoopCondition");

// const auto CondOnLoop =
//     varDecl(unless(hasAncestor(forStmt())), unless(hasAncestor(whileStmt())),
//             unless(hasAncestor(doStmt())))
//         .bind("varDeclExceptLoopCondition");

// const auto IncCond = hasIncrement(anyOf(
//     unaryOperator(hasOperatorName("++"),
//     hasUnaryOperand(declRefExpr(to(varDecl(
//                                              equalsBoundNode("loopVar")))))),
//     cxxOperatorCallExpr(
//         hasOverloadedOperatorName("++"),
//         hasArgument(0,
//         declRefExpr(to(varDecl(equalsBoundNode("loopVar"))))))));

const StatementMatcher ForCondMatcher =
    binaryOperator(
        hasOperatorName("<"),
        hasLHS(ignoringParenImpCasts(
            declRefExpr(to(varDecl(hasType(isInteger())).bind("loopVar"))))),
        // hasRHS(expr(hasType(isInteger()))),
        hasParent(forStmt(hasCondition(expr().bind("forCondition")))))
        .bind("forCondition");

const RewriteRule ForCond1024Rule =
    makeRule(ForCondMatcher, changeTo(cat(name("loopVar"), " < 4096")));

// FIXME: dynamic variable matcher exists?
auto makeNDimensionalArrayMatcher(unsigned n) {
  if (n == 0) {
    return varDecl(hasType(isInteger())).bind("var");
  }

  // FIXME: builtin types ok? or shold I enumerate stdint.h types?
  auto ArrayMatcher =
      constantArrayType(hasElementType(anyOf(isInteger(), builtinType())))
          .bind("arrayType");
  for (unsigned i = 1; i < n; ++i) {
    ArrayMatcher = constantArrayType(hasElementType(ArrayMatcher));
  }

  return varDecl(hasType(ArrayMatcher),
                 optionally(
                     hasInitializer(initListExpr().bind("arrayInitializer"))))
      .bind("nDimArray");
}

auto makeNDArrayAlignedAndEnlargedRule(unsigned n) {
  std::string NewSize = "";
  for (unsigned i = 0; i < n; i++)
    NewSize += "[4096]";

  return makeRule(
      makeNDimensionalArrayMatcher(n),
      flatten(ifBound(
          "arrayInitializer",
          // FIXME: how to get type from AST currently, alignas is dupped.
          changeTo(cat("alignas(128) ",
                       between(before(node("nDimArray")), name("nDimArray")),
                       name("nDimArray"), NewSize, "=",
                       node("arrayInitializer"), ";")),
          changeTo(cat("alignas(128) ",
                       between(before(node("nDimArray")), name("nDimArray")),
                       name("nDimArray"), NewSize, ";")))));
}
const RewriteRule AlignAndEnlargeArrayRule1 =
    makeNDArrayAlignedAndEnlargedRule(3);

class MatchCollector : public MatchFinder::MatchCallback {
private:
  clang::transformer::RewriteRule Rule;
  // this is from Tool.
  std::map<std::string, clang::tooling::Replacements> &FileToReplaces;

public:
  MatchCollector(
      const RewriteRule _Rule,
      std::map<std::string, clang::tooling::Replacements> &_FileToReplaces)
      : Rule(_Rule), FileToReplaces(_FileToReplaces) {}

  inline const RewriteRule &getRule() { return Rule; }

  void run(const MatchFinder::MatchResult &Result) override {
    if (Result.Context->getDiagnostics().hasErrorOccurred()) {
      llvm::errs() << "An error has occurred.\n";
      return;
    }
    Expected<SmallVector<transformer::Edit, 1>> Edits =
        Rule.Cases[findSelectedCase(Result, Rule)].Edits(Result);
    if (!Edits) {
      llvm::errs() << "Rewrite failed: " << llvm::toString(Edits.takeError())
                   << "\n";
      return;
    }
    const SourceManager *SM = Result.SourceManager;
    for (const auto &T : *Edits) {
      assert(T.Kind == EditKind::Range);
      llvm::errs() << "Replacement is " << T.Replacement << "\n";
      // TODO: Add this to Replacements
      // Add Replacement to Replacements
      Replacement Rep(*SM, T.Range, T.Replacement);
      auto &Replaces = FileToReplaces[std::string(Rep.getFilePath())];
      llvm::errs() << "Offset" << Rep.getOffset() << "\n";
      llvm::errs() << "Length" << Rep.getLength() << "\n";
      if (auto Err = Replaces.add(Rep)) {
        unsigned NewOffset = Replaces.getShiftedCodePosition(Rep.getOffset());
        unsigned NewLength =
            Replaces.getShiftedCodePosition(Rep.getOffset() + Rep.getLength()) -
            NewOffset;

        llvm::errs() << "NewOffset=" << NewOffset << "\n";
        llvm::errs() << "NewLength=" << NewLength << "\n";
        if (NewLength == Rep.getLength()) {
          Rep = Replacement(Rep.getFilePath(), NewOffset, NewLength,
                            Rep.getReplacementText());
          // Replaces = Replaces.merge(tooling::Replacements(Rep));
          auto Err2 = Replaces.add(Rep);
          assert(!Err2 && "unresolvable conflicts!");
        } else {
          llvm_unreachable(llvm::toString(std::move(Err)).c_str());
        }
      }
    }
  }
};

// Apply a custom category to all command-line options so that they are the
// only ones displayed.
static cl::OptionCategory MyToolCategory("my-tool options");

int main(int argc, const char **argv) {
  // CommonOptionsParser constructor will parse arguments and create a
  // CompilationDatabase.  In case of error it will terminate the program.
  llvm::errs() << argc;
  for (int i = 0; i < argc; i++)
    llvm::errs() << std::string(argv[i]) << ", ";
  llvm::Expected<CommonOptionsParser> Expected =
      CommonOptionsParser::create(argc, argv, MyToolCategory);
  if (!Expected) {
    llvm::errs() << Expected.takeError();
    return 1;
  }
  CommonOptionsParser &OptionsParser = Expected.get();

  RefactoringTool Tool(OptionsParser.getCompilations(),
                       OptionsParser.getSourcePathList());

  MatchFinder Finder;
  // MatchCollector LC(IncLoopTo1024LoopRule, Tool.getReplacements());
  // MatchCollector UC(UnnestedLoopTo1024LoopRule, Tool.getReplacements());
  MatchCollector FC(AlignAndEnlargeArrayRule1, Tool.getReplacements());
  // Match, Replace collector

  for (auto &Matcher : buildMatchers(FC.getRule())) {
    llvm::errs() << "adding Matcher"
                 << "\n";
    Finder.addDynamicMatcher(
        Matcher.withTraversalKind(TK_IgnoreUnlessSpelledInSource), &FC);
  }

  int Exit = Tool.run(newFrontendActionFactory(&Finder).get());
  if (Exit) {
    llvm::errs() << "Tool.run exits with :" << Exit << "\n";
    return 1;
  }

  // apply replacements
  LangOptions DefaultLangOptions;
  IntrusiveRefCntPtr<DiagnosticOptions> DiagOpts = new DiagnosticOptions();
  clang::TextDiagnosticPrinter DiagnosticPrinter(errs(), &*DiagOpts);
  DiagnosticsEngine Diagnostics(
      IntrusiveRefCntPtr<DiagnosticIDs>(new DiagnosticIDs()), &*DiagOpts,
      &DiagnosticPrinter, false);
  auto &FileMgr = Tool.getFiles();
  SourceManager Sources(Diagnostics, FileMgr);

  Rewriter Rewrite(Sources, DefaultLangOptions);

  errs() << "Num replacements: " << Tool.getReplacements().size() << "\n";

  bool Result = true;
  for (const auto &FileAndReplaces : groupReplacementsByFile(
           Rewrite.getSourceMgr().getFileManager(), Tool.getReplacements())) {
    // FIXME: don't replace csmith
    llvm::errs() << "replace " + FileAndReplaces.first << "\n";
    const Replacements &CurReplaces = FileAndReplaces.second;

    for (auto &R : CurReplaces) {
      llvm::errs() << "text = " << R.getReplacementText() << "\n";
    }

    Result = applyAllReplacements(CurReplaces, Rewrite) && Result;
  }
  if (!Result) {
    llvm::errs() << "Failed applying all replacements.\n";
    return 1;
  }

  return !Rewrite.overwriteChangedFiles();
}
