import Batteries.Data.Rat.Basic
import Init.Data.Int.DivMod

def Rat.frac (r : Rat) : Rat :=
  mkRat (r.num % r.den) r.den

def update : Nat → List Rat → List Rat
| _, [] => []
| 0, xs => xs
| n+1, x :: xs =>
  let ys := xs.map fun y ↦ (-y / x).frac
  let y  := (1 / x).frac
  match y with
  | 0 => y :: (update n ys)
  | _ => update n (y :: ys)

def fib : Nat → Nat 
| 0 => 1
| 1 => 1
| n + 2 => fib n + fib (n + 1)

def seq' : Nat → List Nat
| 0 => [0]
| (n + 1) => (n + 1) :: seq' n

def seq i := (seq' i).reverse

def n := 12
def m := 12
variable (b : Nat)
def foo := [
  mkRat (fib (2 * n)) 
        (fib (2 * n + 1)), 
  mkRat ((fib (m + 1)) * (fib (2 * n + 1)) + fib m) 
        ((fib (m + 1)) * fib (2 * n + 1))]

#eval (seq (2 * n + m)).map fun n ↦ (n, update n foo)
