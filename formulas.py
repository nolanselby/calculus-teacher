FORMULAS = {
    "calc1": {
        "label": "Calc 1",
        "overview": "Calculus 1 introduces the two big ideas of calculus: the derivative (instantaneous rate of change) and the integral (accumulated area). You'll start with limits — the foundation everything else is built on — then learn to differentiate and integrate functions.",
        "categories": [
            {
                "name": "Limits",
                "icon": "bi-arrow-right-circle",
                "formulas": [
                    {
                        "name": "Limit Definition",
                        "formula": r"\lim_{x \to a} f(x) = L",
                        "meaning": "As x gets closer and closer to the value 'a', the function f(x) gets closer and closer to L.",
                        "when": "Use this to understand what a function approaches — even if it never actually reaches that value.",
                        "intuition": "Imagine walking toward a wall — you never reach it, but you can describe exactly where you're headed. The limit is that destination.",
                        "example": {
                            "problem": r"Find \( \lim_{x \to 2} (x^2 + 1) \)",
                            "steps": [r"Plug in x = 2: \( (2)^2 + 1 = 5 \)", r"Since f(x) = x² + 1 is continuous, the limit equals the function value."],
                            "answer": r"\( \lim_{x \to 2} (x^2 + 1) = 5 \)"
                        },
                        "pitfall": "Don't confuse the limit with the actual function value — they can differ at a hole or discontinuity. Always check whether the function is continuous at the point."
                    },
                    {
                        "name": "L'Hôpital's Rule",
                        "formula": r"\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}",
                        "meaning": "When a limit gives you 0/0 or ∞/∞, take the derivative of the top and bottom separately, then try the limit again.",
                        "when": "Use when plugging in the value gives you an indeterminate form like 0/0 or ∞/∞.",
                        "intuition": "If two runners are approaching the finish line at the same time, their ratio of speeds tells you whose ratio is winning — that's what L'Hôpital's Rule captures.",
                        "example": {
                            "problem": r"Find \( \lim_{x \to 0} \dfrac{\sin x}{x} \)",
                            "steps": [
                                r"Plugging in 0 gives 0/0 — indeterminate form.",
                                r"Apply L'Hôpital: differentiate top and bottom separately.",
                                r"\( \lim_{x \to 0} \dfrac{\cos x}{1} \)",
                                r"Plug in 0: \( \cos(0) = 1 \)"
                            ],
                            "answer": r"\( \lim_{x \to 0} \dfrac{\sin x}{x} = 1 \)"
                        },
                        "pitfall": "Only use L'Hôpital when you have 0/0 or ∞/∞. Using it on a normal limit (like 3/5) gives a wrong answer. Always check the form first."
                    },
                    {
                        "name": "Squeeze Theorem",
                        "formula": r"\text{If } g(x) \le f(x) \le h(x) \text{ and } \lim g = \lim h = L, \text{ then } \lim f = L",
                        "meaning": "If a function is always 'squeezed' between two functions that both approach the same limit, then the middle function must approach that limit too.",
                        "when": "Use when dealing with oscillating functions like sin or cos inside a limit that's hard to evaluate directly.",
                        "intuition": "If two friends hold your arms and both walk to the same door, you have no choice but to arrive at that door too — you're squeezed between them.",
                        "example": {
                            "problem": r"Find \( \lim_{x \to 0} x^2 \sin\!\left(\tfrac{1}{x}\right) \)",
                            "steps": [
                                r"We know \( -1 \le \sin\!\left(\tfrac{1}{x}\right) \le 1 \) always.",
                                r"Multiply by x²: \( -x^2 \le x^2\sin(1/x) \le x^2 \)",
                                r"As x → 0, both -x² → 0 and x² → 0.",
                                r"By Squeeze Theorem, the middle term is also squeezed to 0."
                            ],
                            "answer": r"\( \lim_{x \to 0} x^2 \sin(1/x) = 0 \)"
                        },
                        "pitfall": "The bounding functions must have the SAME limit. If they approach different values, the squeeze theorem doesn't apply."
                    },
                    {
                        "name": "Continuity Condition",
                        "formula": r"f \text{ is continuous at } a \iff \lim_{x \to a} f(x) = f(a)",
                        "meaning": "A function is continuous at a point if the limit equals the actual function value — no jumps, holes, or breaks.",
                        "when": "Use to check if a function is continuous at a specific point or to find values that make a piecewise function continuous.",
                        "intuition": "Draw the function without lifting your pencil. If you can, it's continuous. Breaks, holes, or jumps in the graph mean it's not continuous at those points.",
                        "example": {
                            "problem": r"Is \( f(x) = \dfrac{x^2 - 4}{x - 2} \) continuous at x = 2?",
                            "steps": [
                                r"Check f(2): \( \dfrac{4-4}{2-2} = \dfrac{0}{0} \) — undefined! So f(2) doesn't exist.",
                                r"Check the limit: factor numerator: \( \dfrac{(x-2)(x+2)}{x-2} = x+2 \)",
                                r"\( \lim_{x \to 2}(x+2) = 4 \)",
                                r"Since f(2) is undefined, the function is NOT continuous at x = 2 (it has a hole there)."
                            ],
                            "answer": r"Not continuous at x = 2 (removable discontinuity / hole)"
                        },
                        "pitfall": "Three conditions must ALL hold: (1) f(a) must exist, (2) the limit must exist, (3) they must be equal. Failing any one means it's not continuous."
                    }
                ]
            },
            {
                "name": "Derivatives",
                "icon": "bi-graph-up",
                "formulas": [
                    {
                        "name": "Power Rule",
                        "formula": r"\frac{d}{dx}[x^n] = nx^{n-1}",
                        "meaning": "Bring the exponent down as a multiplier, then subtract 1 from the exponent.",
                        "when": "Use for any term that's x raised to a power: x², x³, x^(1/2), etc.",
                        "intuition": "Think of x^n as x multiplied by itself n times. The power rule counts: differentiate any one of those copies and multiply by n (the number of copies).",
                        "example": {
                            "problem": r"Find the derivative of \( f(x) = 4x^3 - 2x^2 + 7x - 5 \)",
                            "steps": [
                                r"Apply the power rule to each term separately.",
                                r"\( \dfrac{d}{dx}[4x^3] = 4 \cdot 3x^2 = 12x^2 \)",
                                r"\( \dfrac{d}{dx}[-2x^2] = -2 \cdot 2x = -4x \)",
                                r"\( \dfrac{d}{dx}[7x] = 7 \), and constants → 0"
                            ],
                            "answer": r"\( f'(x) = 12x^2 - 4x + 7 \)"
                        },
                        "pitfall": "Don't forget the coefficient! The rule is nxⁿ⁻¹ — multiply the existing coefficient by n. Also: the derivative of a constant is 0, not 1."
                    },
                    {
                        "name": "Product Rule",
                        "formula": r"\frac{d}{dx}[f \cdot g] = f'g + fg'",
                        "meaning": "Derivative of the first times the second, plus the first times the derivative of the second.",
                        "when": "Use when you're multiplying two functions together (and can't simplify first).",
                        "intuition": "If two things are both changing, the total rate of change of their product is: how fast the first grows × the second's current size, plus the first's current size × how fast the second grows.",
                        "example": {
                            "problem": r"Find \( \dfrac{d}{dx}[x^2 \sin x] \)",
                            "steps": [
                                r"Set f = x² and g = sin x",
                                r"f' = 2x, g' = cos x",
                                r"Product Rule: f'g + fg' = 2x · sin x + x² · cos x"
                            ],
                            "answer": r"\( 2x\sin x + x^2\cos x \)"
                        },
                        "pitfall": "A very common error is writing (fg)' = f'g'. That's WRONG. You must add both terms. The product of derivatives is not the derivative of the product."
                    },
                    {
                        "name": "Quotient Rule",
                        "formula": r"\frac{d}{dx}\left[\frac{f}{g}\right] = \frac{f'g - fg'}{g^2}",
                        "meaning": "Low times d-high minus high times d-low, over the bottom squared. (Low = denominator, High = numerator)",
                        "when": "Use when differentiating a fraction where both top and bottom contain x.",
                        "intuition": "Memory trick: 'low d-high minus high d-low, square the bottom and away we go.' The minus sign makes it crucial to get the order right.",
                        "example": {
                            "problem": r"Find \( \dfrac{d}{dx}\!\left[\dfrac{x^2}{x+1}\right] \)",
                            "steps": [
                                r"f = x², g = x+1; f' = 2x, g' = 1",
                                r"\( \dfrac{f'g - fg'}{g^2} = \dfrac{2x(x+1) - x^2(1)}{(x+1)^2} \)",
                                r"\( = \dfrac{2x^2 + 2x - x^2}{(x+1)^2} = \dfrac{x^2 + 2x}{(x+1)^2} \)"
                            ],
                            "answer": r"\( \dfrac{x^2 + 2x}{(x+1)^2} \)"
                        },
                        "pitfall": "The ORDER MATTERS: it's f'g − fg', NOT fg' − f'g. Getting the order wrong flips the sign of your answer. Also don't forget to square the denominator."
                    },
                    {
                        "name": "Chain Rule",
                        "formula": r"\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)",
                        "meaning": "Derivative of the outside (leaving inside alone) times derivative of the inside.",
                        "when": "Use when one function is nested inside another, like sin(x²) or e^(3x).",
                        "intuition": "If a car's speed depends on time, and time depends on another clock, the car's speed relative to that other clock is the product of both rates. That's the chain rule.",
                        "example": {
                            "problem": r"Find \( \dfrac{d}{dx}[\sin(3x^2)] \)",
                            "steps": [
                                r"Outer function: sin(u), derivative: cos(u)",
                                r"Inner function: u = 3x², derivative: 6x",
                                r"Chain Rule: cos(3x²) · 6x"
                            ],
                            "answer": r"\( 6x\cos(3x^2) \)"
                        },
                        "pitfall": "The most common mistake is forgetting to multiply by the derivative of the inside (g'(x)). Always ask: 'Did I differentiate the inside?'"
                    },
                    {
                        "name": "Common Derivatives",
                        "formula": r"\tfrac{d}{dx}[\sin x] = \cos x \;\; \tfrac{d}{dx}[\cos x] = -\sin x \;\; \tfrac{d}{dx}[e^x] = e^x \;\; \tfrac{d}{dx}[\ln x] = \tfrac{1}{x}",
                        "meaning": "These are the derivatives you just have to memorize — they appear constantly.",
                        "when": "Any time you see sin, cos, e^x, or ln(x) in a problem.",
                        "intuition": "sin and cos chase each other in a cycle (sin→cos→-sin→-cos→sin). The function e^x is special because it is its own derivative — it grows at the same rate as its size.",
                        "example": {
                            "problem": r"Find \( \dfrac{d}{dx}[e^x \cos x] \) using the Product Rule",
                            "steps": [
                                r"f = eˣ, g = cos x",
                                r"f' = eˣ, g' = −sin x",
                                r"Product Rule: eˣ cos x + eˣ(−sin x)"
                            ],
                            "answer": r"\( e^x(\cos x - \sin x) \)"
                        },
                        "pitfall": "Don't confuse: d/dx[cos x] = −sin x (negative!), but d/dx[sin x] = +cos x. The minus sign only appears when differentiating cosine."
                    },
                    {
                        "name": "Derivative Definition",
                        "formula": r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
                        "meaning": "The derivative is the slope of the tangent line — found by taking the limit of the slope between two very close points.",
                        "when": "Use for 'find the derivative from the definition' problems, or to understand what a derivative really means.",
                        "intuition": "Imagine zooming in on a curve at a point until it looks like a straight line — the slope of that line is the derivative. The definition captures this zoom-in process mathematically.",
                        "example": {
                            "problem": r"Use the definition to find \( f'(x) \) for \( f(x) = x^2 \)",
                            "steps": [
                                r"\( \dfrac{f(x+h)-f(x)}{h} = \dfrac{(x+h)^2 - x^2}{h} \)",
                                r"\( = \dfrac{x^2 + 2xh + h^2 - x^2}{h} = \dfrac{2xh + h^2}{h} \)",
                                r"Factor: \( \dfrac{h(2x+h)}{h} = 2x + h \)",
                                r"Take the limit as h → 0: \( 2x + 0 = 2x \)"
                            ],
                            "answer": r"\( f'(x) = 2x \)"
                        },
                        "pitfall": "Students often forget to take the limit at the end — you MUST let h → 0. Also, be careful expanding (x+h)²: it's x² + 2xh + h², NOT x² + h²."
                    }
                ]
            },
            {
                "name": "Applications of Derivatives",
                "icon": "bi-bar-chart-line",
                "formulas": [
                    {
                        "name": "Mean Value Theorem",
                        "formula": r"f'(c) = \frac{f(b) - f(a)}{b - a} \text{ for some } c \in (a,b)",
                        "meaning": "If a function is smooth and continuous on an interval, there's always at least one point where the instantaneous slope equals the average slope.",
                        "when": "Use to prove a certain slope exists, or in problems asking you to find a guaranteed point c.",
                        "intuition": "If you drive 120 miles in 2 hours, your average speed is 60 mph. The MVT says at some moment during that drive, your speedometer read exactly 60 mph.",
                        "example": {
                            "problem": r"Find c guaranteed by MVT for \( f(x) = x^2 \) on [1, 3]",
                            "steps": [
                                r"Average slope: \( \dfrac{f(3)-f(1)}{3-1} = \dfrac{9-1}{2} = 4 \)",
                                r"Set f'(c) = 4: \( 2c = 4 \Rightarrow c = 2 \)",
                                r"Check: c = 2 is in (1, 3) ✓"
                            ],
                            "answer": r"\( c = 2 \)"
                        },
                        "pitfall": "MVT requires the function to be continuous on [a,b] AND differentiable on (a,b). If either condition fails, MVT may not apply."
                    },
                    {
                        "name": "Critical Points",
                        "formula": r"f'(x) = 0 \text{ or } f'(x) \text{ is undefined}",
                        "meaning": "Critical points are where the function could have a max, min, or flat spot — found where the derivative is zero or doesn't exist.",
                        "when": "Use to find local maximums and minimums in optimization or curve-sketching problems.",
                        "intuition": "At the peak of a hill or the bottom of a valley, the slope is zero — the ground is momentarily flat. Critical points are exactly those flat (or undefined) spots.",
                        "example": {
                            "problem": r"Find the critical points of \( f(x) = x^3 - 3x \)",
                            "steps": [
                                r"f'(x) = 3x² − 3",
                                r"Set f'(x) = 0: 3x² − 3 = 0 → x² = 1 → x = ±1",
                                r"f'(x) is defined everywhere, so no additional critical points."
                            ],
                            "answer": r"\( x = -1 \) and \( x = 1 \)"
                        },
                        "pitfall": "Critical points are where f'(x) = 0 or undefined — NOT where f(x) = 0. Also, a critical point is not automatically a max or min; it could be an inflection point."
                    },
                    {
                        "name": "Concavity (Second Derivative Test)",
                        "formula": r"f''(x) > 0 \Rightarrow \text{concave up} \quad f''(x) < 0 \Rightarrow \text{concave down}",
                        "meaning": "The second derivative tells you whether the curve is cupping upward (like a bowl) or downward (like a hill).",
                        "when": "Use to confirm whether a critical point is a local min (concave up) or local max (concave down).",
                        "intuition": "If you're on a road that curves upward like a bowl, you'd say you're in a valley. If it curves down like an arch, you're on a hill. That curvature is exactly what the second derivative measures.",
                        "example": {
                            "problem": r"For \( f(x) = x^3 - 3x \), classify the critical points x = ±1",
                            "steps": [
                                r"f''(x) = 6x",
                                r"At x = −1: f''(−1) = −6 < 0 → concave down → local MAX",
                                r"At x = 1: f''(1) = 6 > 0 → concave up → local MIN"
                            ],
                            "answer": r"Local max at \( x = -1 \), local min at \( x = 1 \)"
                        },
                        "pitfall": "If f''(c) = 0, the second derivative test is INCONCLUSIVE — you must use the first derivative test instead. Don't assume it's an inflection point automatically."
                    }
                ]
            },
            {
                "name": "Integrals",
                "icon": "bi-infinity",
                "formulas": [
                    {
                        "name": "Fundamental Theorem of Calculus (Part 1)",
                        "formula": r"\frac{d}{dx}\int_a^x f(t)\,dt = f(x)",
                        "meaning": "Taking the derivative of an integral (with x as the upper limit) gives you back the original function.",
                        "when": "Use when you need to differentiate an integral with a variable upper bound.",
                        "intuition": "The integral accumulates area up to x. The derivative asks 'how fast is it accumulating?' The answer is exactly the height of the function at x — that's f(x).",
                        "example": {
                            "problem": r"Find \( \dfrac{d}{dx}\int_0^x \cos(t^2)\,dt \)",
                            "steps": [
                                r"FTC Part 1: differentiate the integral → just replace t with x in the integrand.",
                            ],
                            "answer": r"\( \cos(x^2) \)"
                        },
                        "pitfall": "If the upper limit is NOT just x (e.g., it's x²), you MUST use the chain rule: multiply by the derivative of the upper limit."
                    },
                    {
                        "name": "Fundamental Theorem of Calculus (Part 2)",
                        "formula": r"\int_a^b f(x)\,dx = F(b) - F(a)",
                        "meaning": "To evaluate a definite integral, find the antiderivative, then subtract the value at the bottom from the value at the top.",
                        "when": "Use to evaluate any definite integral once you have the antiderivative.",
                        "intuition": "The net area under a curve from a to b depends only on the starting and ending values of the antiderivative — everything in between cancels out perfectly.",
                        "example": {
                            "problem": r"Evaluate \( \displaystyle\int_1^3 x^2\,dx \)",
                            "steps": [
                                r"Antiderivative: F(x) = x³/3",
                                r"F(3) − F(1) = 27/3 − 1/3 = 9 − 1/3"
                            ],
                            "answer": r"\( \dfrac{26}{3} \)"
                        },
                        "pitfall": "Write F(b) − F(a), not F(a) − F(b). The order matters! Also don't forget to evaluate at both endpoints — students sometimes only evaluate at the top."
                    },
                    {
                        "name": "Power Rule (Integration)",
                        "formula": r"\int x^n\,dx = \frac{x^{n+1}}{n+1} + C \quad (n \ne -1)",
                        "meaning": "Add 1 to the exponent, then divide by that new exponent. Always add +C for indefinite integrals.",
                        "when": "Use for integrating any power of x — the reverse of the derivative power rule.",
                        "intuition": "Integration is the opposite of differentiation. The power rule in reverse: instead of multiplying by n and subtracting 1, you add 1 to the power and divide by the new power.",
                        "example": {
                            "problem": r"Find \( \displaystyle\int (3x^2 + 4x - 1)\,dx \)",
                            "steps": [
                                r"\( \int 3x^2\,dx = 3 \cdot \dfrac{x^3}{3} = x^3 \)",
                                r"\( \int 4x\,dx = 4 \cdot \dfrac{x^2}{2} = 2x^2 \)",
                                r"\( \int (-1)\,dx = -x \)"
                            ],
                            "answer": r"\( x^3 + 2x^2 - x + C \)"
                        },
                        "pitfall": "The rule fails for n = −1 (that's ∫(1/x)dx = ln|x| + C, a special case). Also NEVER forget the + C on indefinite integrals — it's worth points."
                    },
                    {
                        "name": "Common Integrals",
                        "formula": r"\int e^x\,dx = e^x + C \;\; \int \tfrac{1}{x}\,dx = \ln|x| + C \;\; \int \sin x\,dx = -\cos x + C \;\; \int \cos x\,dx = \sin x + C",
                        "meaning": "These are standard antiderivatives you need to memorize — they come up in almost every problem.",
                        "when": "Any time you see e^x, 1/x, sin(x), or cos(x) being integrated.",
                        "intuition": "These come directly from reversing the common derivatives. Because d/dx[e^x] = e^x, its integral is itself. Because d/dx[−cos x] = sin x, the integral of sin x is −cos x.",
                        "example": {
                            "problem": r"Evaluate \( \displaystyle\int_0^\pi \sin x\,dx \)",
                            "steps": [
                                r"Antiderivative of sin x is −cos x",
                                r"[−cos x] from 0 to π: −cos(π) − (−cos(0))",
                                r"= −(−1) − (−1) = 1 + 1"
                            ],
                            "answer": r"\( 2 \)"
                        },
                        "pitfall": "Note the minus sign: ∫sin x dx = −cos x + C (not +cos x). A classic sign error that shows up on every exam."
                    }
                ]
            }
        ]
    },
    "calc2": {
        "label": "Calc 2",
        "overview": "Calculus 2 deepens your integration toolkit with advanced techniques (u-sub, integration by parts, trig substitution) and applies integrals to real geometry (volumes, arc length). You'll also study sequences and series — powerful tools for approximating functions with polynomials.",
        "categories": [
            {
                "name": "Integration Techniques",
                "icon": "bi-tools",
                "formulas": [
                    {
                        "name": "U-Substitution",
                        "formula": r"\int f(g(x))g'(x)\,dx = \int f(u)\,du \quad \text{where } u = g(x)",
                        "meaning": "Let u equal the 'inner function', find du, substitute everything in terms of u, integrate, then sub back.",
                        "when": "Use when you spot a function and its derivative both inside the integral.",
                        "intuition": "U-substitution is the reverse of the chain rule. If you see a function and its derivative sitting next to each other, they want to be grouped into a single variable.",
                        "example": {
                            "problem": r"Find \( \displaystyle\int 2x\cos(x^2)\,dx \)",
                            "steps": [
                                r"Let u = x², then du = 2x dx",
                                r"Substitute: \( \int \cos(u)\,du \)",
                                r"Integrate: sin(u) + C",
                                r"Back-substitute: sin(x²) + C"
                            ],
                            "answer": r"\( \sin(x^2) + C \)"
                        },
                        "pitfall": "You must account for ALL parts of the dx substitution. If your du doesn't match perfectly, try adjusting by a constant factor, but never adjust by a variable."
                    },
                    {
                        "name": "Integration by Parts",
                        "formula": r"\int u\,dv = uv - \int v\,du",
                        "meaning": "Pick one part to be 'u' and the other to be 'dv'. Differentiate u and integrate dv. Then apply the formula.",
                        "when": "Use for products of different types of functions — like x·sin(x), x·eˣ, or ln(x)·x². Remember LIATE for choosing u.",
                        "intuition": "LIATE priority for choosing u: Logarithm, Inverse trig, Algebraic (xⁿ), Trig, Exponential. Choose u as the type that comes earlier in LIATE.",
                        "example": {
                            "problem": r"Find \( \displaystyle\int x e^x\,dx \)",
                            "steps": [
                                r"u = x (algebraic, earlier in LIATE), dv = eˣ dx",
                                r"du = dx, v = eˣ",
                                r"\( uv - \int v\,du = xe^x - \int e^x\,dx \)",
                                r"= xeˣ − eˣ + C"
                            ],
                            "answer": r"\( e^x(x - 1) + C \)"
                        },
                        "pitfall": "After applying integration by parts once, the new integral ∫v du must be simpler than what you started with. If it's more complex, you probably chose u and dv backwards."
                    },
                    {
                        "name": "Trigonometric Substitution",
                        "formula": r"\sqrt{a^2 - x^2} \Rightarrow x = a\sin\theta \;\; \sqrt{a^2 + x^2} \Rightarrow x = a\tan\theta \;\; \sqrt{x^2 - a^2} \Rightarrow x = a\sec\theta",
                        "meaning": "Swap x for a trig function to eliminate the square root, use trig identities to simplify, integrate, then convert back.",
                        "when": "Use when you see a square root of the form √(a²-x²), √(a²+x²), or √(x²-a²).",
                        "intuition": "These substitutions use the Pythagorean identities sin²+cos²=1, tan²+1=sec². The right triangle picture makes it clear which sides correspond to which parts of the expression.",
                        "example": {
                            "problem": r"Find \( \displaystyle\int \sqrt{4 - x^2}\,dx \)",
                            "steps": [
                                r"Form √(a²−x²) with a=2: let x = 2sinθ, dx = 2cosθ dθ",
                                r"\( \sqrt{4 - 4\sin^2\theta} = 2\cos\theta \)",
                                r"\( \int 2\cos\theta \cdot 2\cos\theta\,d\theta = 4\int\cos^2\theta\,d\theta \)",
                                r"Use half-angle identity, integrate, then convert back to x."
                            ],
                            "answer": r"\( \dfrac{x\sqrt{4-x^2}}{2} + 2\arcsin\!\left(\dfrac{x}{2}\right) + C \)"
                        },
                        "pitfall": "Don't forget to convert EVERYTHING back to x at the end (including dx → dθ and the √ expression). Draw the reference triangle to make back-substitution easier."
                    },
                    {
                        "name": "Partial Fraction Decomposition",
                        "formula": r"\frac{P(x)}{(x-a)(x-b)} = \frac{A}{x-a} + \frac{B}{x-b}",
                        "meaning": "Break a complicated rational fraction into simpler fractions that are easier to integrate.",
                        "when": "Use when integrating a rational function (polynomial over polynomial) where the denominator can be factored.",
                        "intuition": "It's the reverse of adding fractions. Instead of combining 1/(x-1) + 1/(x+1) into one fraction, you split a complicated fraction back into two simple ones.",
                        "example": {
                            "problem": r"Find \( \displaystyle\int \frac{1}{x^2 - 1}\,dx \)",
                            "steps": [
                                r"Factor: x² − 1 = (x−1)(x+1)",
                                r"\( \dfrac{1}{(x-1)(x+1)} = \dfrac{A}{x-1} + \dfrac{B}{x+1} \)",
                                r"Multiply both sides by (x−1)(x+1), plug in x = 1 → A = 1/2; plug in x = −1 → B = −1/2",
                                r"\( \int \dfrac{1/2}{x-1} - \dfrac{1/2}{x+1}\,dx = \dfrac{1}{2}\ln|x-1| - \dfrac{1}{2}\ln|x+1| + C \)"
                            ],
                            "answer": r"\( \dfrac{1}{2}\ln\!\left|\dfrac{x-1}{x+1}\right| + C \)"
                        },
                        "pitfall": "If the degree of the numerator ≥ degree of denominator, you must do polynomial long division FIRST before attempting partial fractions."
                    }
                ]
            },
            {
                "name": "Applications of Integration",
                "icon": "bi-bounding-box",
                "formulas": [
                    {
                        "name": "Area Between Curves",
                        "formula": r"A = \int_a^b [f(x) - g(x)]\,dx \quad \text{where } f(x) \ge g(x)",
                        "meaning": "Integrate the top function minus the bottom function over the interval. The result is the area trapped between them.",
                        "when": "Use when finding the area of a region bounded by two curves.",
                        "intuition": "The area between two curves is like stacking infinitely thin horizontal strips of height (top − bottom). Integrating adds them all up.",
                        "example": {
                            "problem": r"Find the area between \( y = x^2 \) and \( y = x \) on [0,1]",
                            "steps": [
                                r"Check which is on top: at x = 0.5, x = 0.5 > x² = 0.25, so y = x is on top.",
                                r"\( A = \int_0^1 (x - x^2)\,dx = \left[\dfrac{x^2}{2} - \dfrac{x^3}{3}\right]_0^1 \)",
                                r"= 1/2 − 1/3 = 3/6 − 2/6"
                            ],
                            "answer": r"\( A = \dfrac{1}{6} \)"
                        },
                        "pitfall": "Always identify which function is on TOP first. If the curves cross, you must split the integral at the crossing point and handle each piece separately."
                    },
                    {
                        "name": "Disk Method (Volume)",
                        "formula": r"V = \pi \int_a^b [f(x)]^2\,dx",
                        "meaning": "Rotating a curve around the x-axis creates a solid. Integrate π times (radius)² to find its volume.",
                        "when": "Use when rotating a region around the x-axis with no hole in the middle.",
                        "intuition": "Slice the solid into infinitely thin circular disks. Each disk has radius f(x) and thickness dx, giving volume πr²(dx). Add them all up with integration.",
                        "example": {
                            "problem": r"Find the volume when \( y = \sqrt{x} \) is rotated around the x-axis on [0, 4]",
                            "steps": [
                                r"\( V = \pi\int_0^4 (\sqrt{x})^2\,dx = \pi\int_0^4 x\,dx \)",
                                r"\( = \pi\left[\dfrac{x^2}{2}\right]_0^4 = \pi \cdot 8 \)"
                            ],
                            "answer": r"\( 8\pi \)"
                        },
                        "pitfall": "The radius is the y-value (the function output), NOT x. Square the entire function before integrating, not after."
                    },
                    {
                        "name": "Washer Method (Volume)",
                        "formula": r"V = \pi \int_a^b \left([f(x)]^2 - [g(x)]^2\right)dx",
                        "meaning": "Like the disk method, but there's a hole. Subtract the inner radius squared from the outer radius squared.",
                        "when": "Use when rotating a region around an axis and there's a gap (hole) in the resulting solid.",
                        "intuition": "Each cross-section is now a washer (a disk with a hole). Area of a washer = π(R² − r²) where R is outer radius and r is inner radius.",
                        "example": {
                            "problem": r"Rotate the region between \( y=x \) and \( y=x^2 \) around the x-axis on [0,1]",
                            "steps": [
                                r"Outer radius R = x (top curve), inner radius r = x²",
                                r"\( V = \pi\int_0^1(x^2 - x^4)\,dx \)",
                                r"\( = \pi\left[\dfrac{x^3}{3} - \dfrac{x^5}{5}\right]_0^1 = \pi\!\left(\dfrac{1}{3} - \dfrac{1}{5}\right) \)"
                            ],
                            "answer": r"\( \dfrac{2\pi}{15} \)"
                        },
                        "pitfall": "The order matters: it's (outer)² − (inner)², not (inner)² − (outer)². Make sure you correctly identify which curve is farther from the axis."
                    },
                    {
                        "name": "Shell Method (Volume)",
                        "formula": r"V = 2\pi \int_a^b x \cdot f(x)\,dx",
                        "meaning": "Imagine thin cylindrical shells stacking up to form the solid. Integrate 2π times radius times height.",
                        "when": "Use when rotating around the y-axis and integrating with respect to x, or when the washer method would be messy.",
                        "intuition": "Unroll each cylindrical shell into a flat rectangle: its width is f(x), its length is 2πx (the circumference), and its thickness is dx. Multiply and integrate.",
                        "example": {
                            "problem": r"Rotate \( y = x^2 \) around the y-axis on [0, 2]. Find the volume.",
                            "steps": [
                                r"\( V = 2\pi\int_0^2 x \cdot x^2\,dx = 2\pi\int_0^2 x^3\,dx \)",
                                r"\( = 2\pi\left[\dfrac{x^4}{4}\right]_0^2 = 2\pi \cdot 4 = 8\pi \)"
                            ],
                            "answer": r"\( 8\pi \)"
                        },
                        "pitfall": "Use the shell method when rotating around the y-axis and your function is already given in terms of x. Trying to use the disk/washer method here would require solving for x in terms of y first."
                    },
                    {
                        "name": "Arc Length",
                        "formula": r"L = \int_a^b \sqrt{1 + [f'(x)]^2}\,dx",
                        "meaning": "The length of a curve is found by integrating tiny straight-line segments along the curve using the Pythagorean theorem.",
                        "when": "Use to find the actual length of a curve between two x-values.",
                        "intuition": "Approximate the curve with tiny line segments. Each segment has length √(dx² + dy²) = √(1 + (dy/dx)²) dx. Integrating adds up all the tiny lengths.",
                        "example": {
                            "problem": r"Find the arc length of \( y = \dfrac{2}{3}x^{3/2} \) from x = 0 to x = 3",
                            "steps": [
                                r"f'(x) = x^{1/2} = √x",
                                r"\( [f'(x)]^2 = x \)",
                                r"\( L = \int_0^3\sqrt{1+x}\,dx \), let u = 1+x",
                                r"\( = \left[\dfrac{2}{3}(1+x)^{3/2}\right]_0^3 = \dfrac{2}{3}(8 - 1) = \dfrac{14}{3} \)"
                            ],
                            "answer": r"\( L = \dfrac{14}{3} \)"
                        },
                        "pitfall": "Don't forget to compute f'(x) and SQUARE it before adding 1. Students often write √(1 + f'(x)) instead of √(1 + [f'(x)]²) — the square is critical."
                    }
                ]
            },
            {
                "name": "Sequences & Series",
                "icon": "bi-list-ol",
                "formulas": [
                    {
                        "name": "Geometric Series",
                        "formula": r"\sum_{n=0}^{\infty} ar^n = \frac{a}{1-r} \quad \text{if } |r| < 1",
                        "meaning": "A geometric series converges to a/(1-r) when the ratio r is between -1 and 1. Otherwise it diverges.",
                        "when": "Use when you see a series of the form a + ar + ar² + ar³ + ...",
                        "intuition": "If each term is a fixed fraction of the previous one, and that fraction is less than 1, the terms shrink fast enough to add up to a finite number.",
                        "example": {
                            "problem": r"Find the sum: \( \displaystyle\sum_{n=0}^{\infty} \left(\dfrac{1}{3}\right)^n \)",
                            "steps": [
                                r"a = 1 (first term), r = 1/3 (ratio)",
                                r"|r| = 1/3 < 1, so the series converges.",
                                r"Sum = a/(1−r) = 1/(1 − 1/3) = 1/(2/3)"
                            ],
                            "answer": r"\( \dfrac{3}{2} \)"
                        },
                        "pitfall": "The formula only works if |r| < 1. If |r| ≥ 1, the series diverges and there's no finite sum. Always check the ratio first."
                    },
                    {
                        "name": "Ratio Test",
                        "formula": r"L = \lim_{n\to\infty} \left|\frac{a_{n+1}}{a_n}\right| \quad L < 1 \Rightarrow \text{converges}, \; L > 1 \Rightarrow \text{diverges}",
                        "meaning": "Divide consecutive terms and take the limit. If the ratio shrinks (L < 1), the series converges.",
                        "when": "Use for series with factorials, exponentials, or powers — very common and reliable test.",
                        "intuition": "If each term is less than 90% of the previous, the terms are shrinking fast enough. The ratio test measures that percentage in the long run.",
                        "example": {
                            "problem": r"Test \( \displaystyle\sum \dfrac{n!}{2^n} \) for convergence.",
                            "steps": [
                                r"\( L = \lim_{n\to\infty}\left|\dfrac{(n+1)!/2^{n+1}}{n!/2^n}\right| = \lim_{n\to\infty}\dfrac{n+1}{2} = \infty \)",
                                r"L > 1, so the series diverges."
                            ],
                            "answer": r"Diverges"
                        },
                        "pitfall": "If L = 1, the ratio test is INCONCLUSIVE — you need another test. Don't declare convergence or divergence when L = 1."
                    },
                    {
                        "name": "Divergence Test",
                        "formula": r"\text{If } \lim_{n\to\infty} a_n \ne 0, \text{ the series } \sum a_n \text{ diverges}",
                        "meaning": "If the individual terms don't shrink to zero, the series can't possibly converge.",
                        "when": "Always check this first — it's the fastest way to prove a series diverges.",
                        "intuition": "If you're adding numbers and they don't even approach 0, you're adding something significant forever — the sum must grow without bound.",
                        "example": {
                            "problem": r"Does \( \displaystyle\sum \dfrac{n}{n+1} \) converge?",
                            "steps": [
                                r"\( \lim_{n\to\infty}\dfrac{n}{n+1} = 1 \ne 0 \)",
                                r"By the Divergence Test, the series diverges."
                            ],
                            "answer": r"Diverges"
                        },
                        "pitfall": "The Divergence Test can only prove DIVERGENCE. If the terms DO go to 0, the test is inconclusive — the series might still diverge (like the harmonic series 1 + 1/2 + 1/3 + ...)."
                    },
                    {
                        "name": "Taylor Series",
                        "formula": r"f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x-a)^n",
                        "meaning": "Any smooth function can be written as an infinite polynomial using its derivatives at a single point a.",
                        "when": "Use to approximate functions, compute limits, or find power series representations.",
                        "intuition": "A Taylor series is a polynomial that matches a function perfectly at one point, and gets better and better the more terms you include — like zooming out from a single tangent line to a curve that fits tighter and tighter.",
                        "example": {
                            "problem": r"Find the Taylor series for \( f(x) = e^x \) centered at a = 0",
                            "steps": [
                                r"All derivatives of eˣ are eˣ. At x=0: f^(n)(0) = 1 for all n.",
                                r"Series: \( \displaystyle\sum_{n=0}^\infty \dfrac{1}{n!}x^n \)"
                            ],
                            "answer": r"\( e^x = 1 + x + \dfrac{x^2}{2!} + \dfrac{x^3}{3!} + \cdots \)"
                        },
                        "pitfall": "The series only equals f(x) within its radius of convergence. Also don't forget n! in the denominator — it's easy to miss."
                    },
                    {
                        "name": "Maclaurin Series (Common)",
                        "formula": r"e^x = \sum\tfrac{x^n}{n!} \quad \sin x = \sum\tfrac{(-1)^n x^{2n+1}}{(2n+1)!} \quad \cos x = \sum\tfrac{(-1)^n x^{2n}}{(2n)!}",
                        "meaning": "These are the most important Taylor series centered at 0 — memorize them, they appear everywhere.",
                        "when": "Use when working with series representations of e^x, sin(x), or cos(x).",
                        "intuition": "sin(x) only uses odd powers (1, 3, 5,...) with alternating signs. cos(x) only uses even powers (0, 2, 4,...) with alternating signs. eˣ uses ALL powers.",
                        "example": {
                            "problem": r"Use the Maclaurin series to evaluate \( \lim_{x\to 0} \dfrac{1-\cos x}{x^2} \)",
                            "steps": [
                                r"Replace cos x: \( 1 - \left(1 - \dfrac{x^2}{2} + \cdots\right) = \dfrac{x^2}{2} - \cdots \)",
                                r"\( \dfrac{x^2/2 - \cdots}{x^2} \to \dfrac{1}{2} \) as x → 0"
                            ],
                            "answer": r"\( \dfrac{1}{2} \)"
                        },
                        "pitfall": "Make sure you're using the correct formula. eˣ has 1/n! in every term. sin x has only odd powers with (2n+1)! denominators. Mixing them up is a very common error."
                    }
                ]
            }
        ]
    },
    "calc3": {
        "label": "Calc 3",
        "overview": "Calculus 3 extends everything you know to multiple dimensions. Instead of functions of one variable, you work with functions of two or three variables — finding partial derivatives, gradients, and integrating over 2D regions and 3D volumes. You'll also study vector fields and the fundamental theorems that unify them.",
        "categories": [
            {
                "name": "Vectors & 3D Space",
                "icon": "bi-box",
                "formulas": [
                    {
                        "name": "Dot Product",
                        "formula": r"\mathbf{a} \cdot \mathbf{b} = a_1b_1 + a_2b_2 + a_3b_3 = |\mathbf{a}||\mathbf{b}|\cos\theta",
                        "meaning": "Multiply matching components and add. The result is a number (scalar) that tells you how much the vectors point in the same direction.",
                        "when": "Use to find the angle between vectors, check if vectors are perpendicular (dot product = 0), or find projections.",
                        "intuition": "The dot product measures how much two vectors 'agree' in direction. If they point the same way it's large and positive; if perpendicular it's 0; if opposite it's negative.",
                        "example": {
                            "problem": r"Find the angle between \( \mathbf{a} = \langle 1,2,2\rangle \) and \( \mathbf{b} = \langle 2,1,-2\rangle \)",
                            "steps": [
                                r"\( \mathbf{a}\cdot\mathbf{b} = 1(2)+2(1)+2(-2) = 2+2-4=0 \)",
                                r"Since the dot product is 0, the vectors are perpendicular."
                            ],
                            "answer": r"\( \theta = 90° \)"
                        },
                        "pitfall": "The dot product gives a SCALAR, not a vector. If you need a perpendicular vector, use the cross product instead."
                    },
                    {
                        "name": "Cross Product",
                        "formula": r"\mathbf{a} \times \mathbf{b} = \begin{vmatrix}\mathbf{i}&\mathbf{j}&\mathbf{k}\\a_1&a_2&a_3\\b_1&b_2&b_3\end{vmatrix}",
                        "meaning": "The cross product gives a new vector that is perpendicular to both original vectors. Its magnitude equals the area of the parallelogram they form.",
                        "when": "Use to find a vector perpendicular to two given vectors, or to find area of parallelograms and triangles in 3D.",
                        "intuition": "Point your fingers along a, curl them toward b — your thumb points in the direction of a × b. This right-hand rule always works.",
                        "example": {
                            "problem": r"Find \( \langle 1,0,0\rangle \times \langle 0,1,0\rangle \)",
                            "steps": [
                                r"\( \begin{vmatrix}\mathbf{i}&\mathbf{j}&\mathbf{k}\\1&0&0\\0&1&0\end{vmatrix} \)",
                                r"\( = \mathbf{i}(0\cdot0 - 0\cdot1) - \mathbf{j}(1\cdot0-0\cdot0) + \mathbf{k}(1\cdot1-0\cdot0) \)",
                                r"= ⟨0, 0, 1⟩ (which is the z-axis direction, k)"
                            ],
                            "answer": r"\( \mathbf{k} = \langle 0,0,1\rangle \)"
                        },
                        "pitfall": "a × b ≠ b × a — cross products are anti-commutative: a × b = −(b × a). Getting the order wrong flips the direction of the result."
                    },
                    {
                        "name": "Equation of a Plane",
                        "formula": r"a(x - x_0) + b(y - y_0) + c(z - z_0) = 0",
                        "meaning": "A plane is defined by a point on it and a normal vector ⟨a, b, c⟩ pointing straight out of the plane.",
                        "when": "Use to write the equation of a plane given a point and a normal vector (or two vectors in the plane).",
                        "intuition": "A plane is flat, so every vector lying in the plane is perpendicular to the normal. The plane equation just says: any point (x,y,z) in the plane, when connected to the known point, gives a vector perpendicular to the normal.",
                        "example": {
                            "problem": r"Find the plane through (1,2,3) with normal \( \mathbf{n} = \langle 2,-1,4\rangle \)",
                            "steps": [
                                r"Plug into formula: 2(x−1) + (−1)(y−2) + 4(z−3) = 0",
                                r"Expand: 2x − 2 − y + 2 + 4z − 12 = 0",
                                r"Simplify: 2x − y + 4z = 12"
                            ],
                            "answer": r"\( 2x - y + 4z = 12 \)"
                        },
                        "pitfall": "If you're given two vectors IN the plane, you must find the normal first using the cross product. Don't confuse vectors in the plane with the normal vector."
                    }
                ]
            },
            {
                "name": "Partial Derivatives",
                "icon": "bi-sliders",
                "formulas": [
                    {
                        "name": "Partial Derivative",
                        "formula": r"\frac{\partial f}{\partial x}: \text{ differentiate w.r.t. } x\text{, treat all other variables as constants}",
                        "meaning": "A partial derivative measures how fast a function changes in one direction while everything else stays frozen.",
                        "when": "Use any time you have a function of multiple variables and need to find its rate of change in one direction.",
                        "intuition": "If you're hiking on a mountain, the partial derivative with respect to x tells you the slope you'd feel walking east, while the partial with respect to y tells you the slope walking north.",
                        "example": {
                            "problem": r"Find \( \partial f/\partial x \) and \( \partial f/\partial y \) for \( f(x,y) = x^2y + 3y^2 \)",
                            "steps": [
                                r"∂f/∂x: treat y as constant → 2xy + 0 = 2xy",
                                r"∂f/∂y: treat x as constant → x² + 6y"
                            ],
                            "answer": r"\( \partial f/\partial x = 2xy, \quad \partial f/\partial y = x^2 + 6y \)"
                        },
                        "pitfall": "When treating y as a constant, it doesn't differentiate — treat it exactly like a number. Students often accidentally differentiate with respect to both variables at once."
                    },
                    {
                        "name": "Gradient",
                        "formula": r"\nabla f = \left\langle \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}, \frac{\partial f}{\partial z} \right\rangle",
                        "meaning": "The gradient is a vector made of all the partial derivatives. It points in the direction of steepest increase of the function.",
                        "when": "Use to find the direction of steepest ascent, compute directional derivatives, or find normal vectors to surfaces.",
                        "intuition": "If f represents the temperature in a room, ∇f points toward the hottest direction from your current position. It's always perpendicular to the level curves.",
                        "example": {
                            "problem": r"Find \( \nabla f \) at (1,2) for \( f(x,y) = x^2 + xy \)",
                            "steps": [
                                r"∂f/∂x = 2x + y, ∂f/∂y = x",
                                r"At (1,2): ∂f/∂x = 2(1)+2 = 4, ∂f/∂y = 1",
                                r"∇f(1,2) = ⟨4, 1⟩"
                            ],
                            "answer": r"\( \nabla f(1,2) = \langle 4, 1 \rangle \)"
                        },
                        "pitfall": "The gradient is a vector (has direction and magnitude), not a scalar. Don't confuse it with the directional derivative, which is a scalar found by dotting the gradient with a unit vector."
                    },
                    {
                        "name": "Directional Derivative",
                        "formula": r"D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}",
                        "meaning": "The rate of change of a function in any direction you choose — found by dotting the gradient with a unit vector in that direction.",
                        "when": "Use when asked 'how fast is f changing in the direction of vector v?'",
                        "intuition": "The directional derivative is the component of the gradient pointing in your chosen direction — how much of the steepest-ascent direction you're walking along.",
                        "example": {
                            "problem": r"Find \( D_{\mathbf{u}}f \) at (1,2) for \( f = x^2+xy \), in direction \( \mathbf{v}=\langle 3,4\rangle \)",
                            "steps": [
                                r"Unit vector: \( \mathbf{u} = \langle 3/5, 4/5\rangle \)",
                                r"∇f(1,2) = ⟨4,1⟩ (from above)",
                                r"\( D_\mathbf{u}f = \langle 4,1\rangle \cdot \langle 3/5, 4/5\rangle = 12/5 + 4/5 = 16/5 \)"
                            ],
                            "answer": r"\( D_{\mathbf{u}}f = \dfrac{16}{5} \)"
                        },
                        "pitfall": "You MUST use a unit vector (magnitude = 1). Forgetting to normalize v first is the most common error. Divide v by |v| before taking the dot product."
                    },
                    {
                        "name": "Chain Rule (Multivariable)",
                        "formula": r"\frac{dz}{dt} = \frac{\partial z}{\partial x}\frac{dx}{dt} + \frac{\partial z}{\partial y}\frac{dy}{dt}",
                        "meaning": "When z depends on x and y, and x and y both depend on t, multiply each partial derivative by the corresponding rate of change.",
                        "when": "Use when a multivariable function's inputs are themselves functions of another variable.",
                        "intuition": "Like compound interest: z changes as x changes (at rate ∂z/∂x), AND as y changes (at rate ∂z/∂y). Add both contributions to get the total rate of change.",
                        "example": {
                            "problem": r"If \(z = x^2+y^2\), \(x=\cos t\), \(y=\sin t\), find \(dz/dt\)",
                            "steps": [
                                r"∂z/∂x = 2x, ∂z/∂y = 2y, dx/dt = −sin t, dy/dt = cos t",
                                r"\( \dfrac{dz}{dt} = 2x(-\sin t) + 2y(\cos t) \)",
                                r"Substitute x = cos t, y = sin t: = −2cos t sin t + 2sin t cos t = 0"
                            ],
                            "answer": r"\( dz/dt = 0 \) (z = 1 always, since x²+y²=1 on the unit circle)"
                        },
                        "pitfall": "Draw a tree diagram showing the dependency chain to avoid missing terms. With more variables, it's easy to leave out a path in the chain."
                    }
                ]
            },
            {
                "name": "Multiple Integrals",
                "icon": "bi-grid-3x3",
                "formulas": [
                    {
                        "name": "Double Integral",
                        "formula": r"\iint_R f(x,y)\,dA = \int_a^b \int_c^d f(x,y)\,dy\,dx",
                        "meaning": "Integrate twice — first with respect to one variable (treating the other as constant), then with respect to the other.",
                        "when": "Use to find volumes under surfaces, areas of regions, or average values of 2-variable functions.",
                        "intuition": "Slice the region into vertical strips (fixing x), then integrate each strip from bottom to top (y direction). Then integrate all strips from left to right (x direction).",
                        "example": {
                            "problem": r"Evaluate \( \displaystyle\int_0^1\!\int_0^2 xy\,dy\,dx \)",
                            "steps": [
                                r"Inner integral (hold x constant): \( \int_0^2 xy\,dy = x\cdot\dfrac{y^2}{2}\Big|_0^2 = 2x \)",
                                r"Outer integral: \( \int_0^1 2x\,dx = \left[x^2\right]_0^1 = 1 \)"
                            ],
                            "answer": r"\( 1 \)"
                        },
                        "pitfall": "The limits of integration tell you what bounds each variable. The inner limits may depend on the outer variable (for non-rectangular regions), so be careful about which bounds go where."
                    },
                    {
                        "name": "Double Integral in Polar",
                        "formula": r"\iint_R f(x,y)\,dA = \int_\alpha^\beta \int_{r_1}^{r_2} f(r\cos\theta,\, r\sin\theta)\,r\,dr\,d\theta",
                        "meaning": "In polar coordinates, dA becomes r·dr·dθ (don't forget the extra r!). Use x = r·cos θ, y = r·sin θ.",
                        "when": "Use when the region is a circle, sector, or ring — polar makes the bounds much simpler.",
                        "intuition": "In Cartesian, area elements are rectangles (dx × dy). In polar, they're little 'wedge-rectangles' of area r·dr·dθ — the r factor compensates for coordinates stretching outward.",
                        "example": {
                            "problem": r"Find \( \iint_R (x^2+y^2)\,dA \) where R is the disk \( x^2+y^2 \le 4 \)",
                            "steps": [
                                r"In polar: x²+y² = r², region: 0 ≤ r ≤ 2, 0 ≤ θ ≤ 2π",
                                r"\( \int_0^{2\pi}\!\int_0^2 r^2 \cdot r\,dr\,d\theta = \int_0^{2\pi}\!\int_0^2 r^3\,dr\,d\theta \)",
                                r"\( = \int_0^{2\pi} 4\,d\theta = 8\pi \)"
                            ],
                            "answer": r"\( 8\pi \)"
                        },
                        "pitfall": "The MOST common error: forgetting the extra r in r·dr·dθ. The dA factor in polar coordinates is ALWAYS r dr dθ, not just dr dθ."
                    },
                    {
                        "name": "Triple Integral",
                        "formula": r"\iiint_E f(x,y,z)\,dV = \int\!\!\int\!\!\int f\,dz\,dy\,dx",
                        "meaning": "Integrate three times, one variable at a time, from the inside out.",
                        "when": "Use to find volumes of 3D regions, mass of solid objects, or integrate over a 3D region.",
                        "intuition": "The triple integral stacks infinitely thin boxes (dV = dx dy dz) to fill a 3D region, summing the function's value over every point inside.",
                        "example": {
                            "problem": r"Evaluate \( \displaystyle\int_0^1\!\int_0^1\!\int_0^1 xyz\,dz\,dy\,dx \)",
                            "steps": [
                                r"Innermost (z): \( \int_0^1 xyz\,dz = xy\cdot\dfrac{z^2}{2}\Big|_0^1 = \dfrac{xy}{2} \)",
                                r"Middle (y): \( \int_0^1 \dfrac{xy}{2}\,dy = \dfrac{x}{2}\cdot\dfrac{1}{2} = \dfrac{x}{4} \)",
                                r"Outer (x): \( \int_0^1\dfrac{x}{4}\,dx = \dfrac{1}{8} \)"
                            ],
                            "answer": r"\( \dfrac{1}{8} \)"
                        },
                        "pitfall": "Always work from the INSIDE out. The innermost integral is done first, then the result is fed to the next integral. Mixing up the order of integration changes the meaning."
                    }
                ]
            },
            {
                "name": "Vector Calculus",
                "icon": "bi-wind",
                "formulas": [
                    {
                        "name": "Line Integral",
                        "formula": r"\int_C f\,ds = \int_a^b f(\mathbf{r}(t))|\mathbf{r}'(t)|\,dt",
                        "meaning": "Integrate a function along a curve. Parameterize the curve, then integrate with respect to arc length.",
                        "when": "Use to find work done by a force along a path, or to integrate a function over a curve.",
                        "intuition": "Imagine painting a fence whose height is given by f at each point. The line integral calculates the area of paint on that fence.",
                        "example": {
                            "problem": r"Find \( \int_C x\,ds \) where C is \( \mathbf{r}(t)=\langle t,t\rangle \) for \( t\in[0,1] \)",
                            "steps": [
                                r"|r'(t)| = |⟨1,1⟩| = √2",
                                r"\( \int_0^1 t\cdot\sqrt{2}\,dt = \sqrt{2}\cdot\dfrac{1}{2} = \dfrac{\sqrt{2}}{2} \)"
                            ],
                            "answer": r"\( \dfrac{\sqrt{2}}{2} \)"
                        },
                        "pitfall": "Don't forget to multiply by |r'(t)| (the speed factor). Without it, you're not accounting for how fast the curve moves through space."
                    },
                    {
                        "name": "Green's Theorem",
                        "formula": r"\oint_C P\,dx + Q\,dy = \iint_D \!\left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right)dA",
                        "meaning": "Converts a line integral around a closed curve into a double integral over the enclosed region — often much easier.",
                        "when": "Use to simplify line integrals over closed curves in 2D, or to find area using line integrals.",
                        "intuition": "The net circulation around the boundary equals the total 'rotation' (curl) inside — like summing up all the tiny whirlpools inside the region to get the total circulation around the edge.",
                        "example": {
                            "problem": r"Evaluate \( \oint_C y^2\,dx + x\,dy \) over the unit circle (counterclockwise)",
                            "steps": [
                                r"P = y², Q = x; ∂Q/∂x = 1, ∂P/∂y = 2y",
                                r"\( \iint_D (1 - 2y)\,dA \), D is the unit disk",
                                r"By symmetry, ∬2y dA = 0. So result = ∬1 dA = π(1²) = π"
                            ],
                            "answer": r"\( \pi \)"
                        },
                        "pitfall": "Green's Theorem requires C to be a positively oriented (counterclockwise), simple closed curve. If the curve goes clockwise, flip the sign of the result."
                    },
                    {
                        "name": "Stokes' Theorem",
                        "formula": r"\iint_S (\nabla \times \mathbf{F}) \cdot d\mathbf{S} = \oint_C \mathbf{F} \cdot d\mathbf{r}",
                        "meaning": "Converts a surface integral of a curl into a line integral around the boundary curve of that surface.",
                        "when": "Use to swap between a complicated surface integral and a simpler boundary line integral (or vice versa).",
                        "intuition": "Like Green's Theorem but in 3D: the total rotation (curl) of a vector field through a surface equals the circulation around its boundary edge.",
                        "example": {
                            "problem": r"Strategy for \( \iint_S(\nabla\times\mathbf{F})\cdot d\mathbf{S} \) when S is a complicated surface",
                            "steps": [
                                r"Find the boundary curve C of S",
                                r"Compute \( \oint_C \mathbf{F}\cdot d\mathbf{r} \) instead — often much simpler",
                                r"By Stokes, the two are equal."
                            ],
                            "answer": r"Use the simpler of the two forms"
                        },
                        "pitfall": "The orientation must be consistent: the boundary C must be oriented so that, standing on the surface and walking along C, the surface is to your left (right-hand rule)."
                    },
                    {
                        "name": "Divergence Theorem",
                        "formula": r"\iint_S \mathbf{F} \cdot d\mathbf{S} = \iiint_E (\nabla \cdot \mathbf{F})\,dV",
                        "meaning": "Converts the flux through a closed surface into a triple integral of the divergence over the enclosed volume.",
                        "when": "Use to replace a difficult surface integral with a triple integral, or when the surface is closed (like a sphere).",
                        "intuition": "The total flow out through a closed surface equals the total 'source strength' inside — if more fluid is being created inside than destroyed, it must flow out through the boundary.",
                        "example": {
                            "problem": r"Find the flux of \( \mathbf{F}=\langle x,y,z\rangle \) through the unit sphere",
                            "steps": [
                                r"∇·F = ∂x/∂x + ∂y/∂y + ∂z/∂z = 1 + 1 + 1 = 3",
                                r"\( \iiint_E 3\,dV = 3\cdot\text{Vol(sphere)} = 3\cdot\dfrac{4\pi}{3} \)"
                            ],
                            "answer": r"\( 4\pi \)"
                        },
                        "pitfall": "The Divergence Theorem only applies to CLOSED surfaces (surfaces with no boundary). If the surface has a hole or edge, it's not closed and you can't use this theorem directly."
                    }
                ]
            }
        ]
    }
}
