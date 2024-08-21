# Lam Script

An interpreter for a simple functional programming language
that emphasizes function definitions and lambda expressions, without
variable assignments or mutable state.

###### This project was inspired by [@CodePulse&#39;s](https://www.youtube.com/@CodePulse) Series: **Make YOUR OWN Programming Language**.

## Data Types:

- **INTEGER:** Whole numbers (e.g., -3, 0, 42)
- **BOOLEAN:** True and False

## Operations:

#### Arithmetic Operations (for INTEGERs):

- Addition (+)
- Subtraction (-)
- Multiplication (*)
- Integer division (//)
- Modulo (%)

#### Boolean Operations:

* AND (&&)
* OR (||)
* NOT (!)

#### Comparison Operations:

* Equal to (==)
* Not equal to (!=)
* Greater than (>)
* Less than (<)
* Greater than or equal to (>=)
* Less than or equal to (<=)

## Functions:

- Named function definitions
- Anonymous functions (lambda expressions)
- Function application

## Recursion:

- Support for recursive function calls
- It should support a replacement for while loop.

## Immutability:

- All values are immutable
- No variable assignments or state changes

## Error Types:

- syntax errors
- type errors
- runtime errors

## The BNF

```
<statements> := NEWLINE* <statement> (NEWLINE+ <statement>)* NEWLINE*

<statement> := <bool_expr> | <return> | <continue> | <break>

<bool_expr> := <bool_term> (<low_order_bool_op> <bool_term>)*

<bool_term> := <bool_factor> (<equals> <bool_factor>)*

<bool_factor> := <bool> | <not> <bool_expr> | <comparison_expr>

<comparison_expr> =: <math_expr> (<comperison_op> <math_expr>)*

<math_expr> := <math_term> (<low_order_math_op> <math_term>)*

<math_term> := <math_factor> (<high_order_math_op> <math_factor>)* 

<math_factor> := <low_order_op> <math_expr> | <call>

<call> := <atom> ( <arguments>? )?

<atom> :=  <int> | <identifier> |  ( <bool_expr> ) 
            | <while_expr> | <func_def> 

<while_expr> := while (<bool_expr>) { <bool_expr> }
              | while (<bool_expr>) { NEWLINE <statements> }

<return> := return <bool_expr>? NEWLINE
<continue> := continue
<break> := break

<func_def> := def <identifier> ( <params>? ) { <bool_expr> }
            | def <identifier> ( <params>? ) { NEWLINE <statements> }
            | lite ( <params>? ) <bool_expr>

<params> := <identifier> (, <identifier>)*
<argument> := <bool_expr> (, <bool_expr>)*

<int> :=  <non_zero_dig> <int> | <non_zero_dig> | 0
<non_zero_dig> := 1..9
<high_order_math_op> := * | / | // | %
<low_order_math_op> := + | -

<keywords> := while | lite

<bool> := true | false
<not> := !
<low_order_bool_op> := && | ||
<comperison_op> : < | <= | > | >= | <equals>
<euqels> := == | != 
```

### The Main Design Decisions in the BNF Grammar:

#### 1. Use of Braces for Code Blocks

- **`{ NEWLINE <statements> }`** and **`{ <bool_expr> }`**:
  - Braces `{}` are used to define code blocks, such as in `while` loops and function definitions.
    We knew from the start that we wanted our language to have braces, like in the following code:

    ```
    def test(x,y) {
        return x,y
    }
    ```

    That said, We didn't want every line to end in `;` at all.

#### 2. Newline Sensitivity

- **`NEWLINE`**:
  - Newline plays a key role in how statements are separated. The presence of `NEWLINE*` and `NEWLINE+` indicates that line breaks are important for statement separation.

#### 3. Boolean Expressions
- **`<bool_expr>`**:
  - Boolean expressions can be composed of multiple terms, we used the `<bool_expr>` to define the base expression. That came to be when we realized That arithmetic operations uses `<Comparission expr>` as the base expression, which gives a boolean value. like in the following expression: 
    ```
    !(true) || x < 3
    ```

#### 4. Short-circuit evaluation

- **`<low_order_bool_op> := && | ||`**:
  - Boolean expressions can be combined using `&&` (logical AND) and `||` (logical OR). Because the language doesn't support if statements, we use of short-circuit evaluation to make conditional statements to still be possible. like in the following code:
    ```
    def fact(n) {
        return (n == 0) || (n * fact(n - 1))
    }
    ```

#### 5. Function Definitions with Optional Blocks or `Lite` Expressions

- **`<func_def>`**:
  - Functions can be defined using the `def` keyword, with the flexibility to include either a block of statements or a single boolean expression (using `lite`). This allows for both concise one-liners and more complex function definitions.

#### 6. Support for While Loops

- **`<while_expr>`**:
  - The language includes a `while` loop expression, where conditions are enclosed in parentheses and loop bodies are defined inside braces. We also added support for `break` and `continue` statements to control loop flow. Like in the following code:
    ```
    def fact_nsc(n) {
        while (n == 0) {
            return 1
        }
        return n * fact_nsc(n - 1)
    }
    ```

#### 7. Optional Elements in Function Calls and Definitions

- **`<call> := <atom> ( <arguments>? )?`**:
  - Function calls and definitions allow for optional arguments and parameters, providing flexibility in how functions are written and invoked.

#### 8. Keywords
- **`<keywords>`**:
    - We decided to chnage conventional keywords. For example: `lite` **instead of** `lambda` to make the language more unique. but still, we kept the `while` is order to fit with the language design standards.
