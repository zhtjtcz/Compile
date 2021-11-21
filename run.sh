clang -emit-llvm -S libsysy.c -o lib.ll
llvm-link test.ll lib.ll -S -o out.ll
lli out.ll
echo $?