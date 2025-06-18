; Created by Cristian Berceanu, Ioan Marica, Monica Patrascu
; (c) Complex Systems Laboratory, University Politehnica of Bucharest Romania
; Contact: cristi92b@gmail.com

breed [susceptible susceptible-agents]
breed [exposed exposed-agents]
breed [infected infected-agents]
breed [immune immune-agents]
turtles-own [energy]
patches-own [information]


globals
[
  run-seed
]

to setup
  clear-all
  ;setup-susceptible
  setup-globals
  setup-susceptible-static
  setup-infected-static
  setup-exposed-static
  setup-immune-static
  setup-patches
  reset-ticks
end

to setup-globals
  set run-seed new-seed random-seed run-seed
end

;to setup-susceptible
;  create-susceptible number-susceptible
;  [
;    setxy random-pxcor random-pycor
;    set heading random 360
;    set color orange
;    set energy agent-starting-energy
;  ]
;end

to setup-susceptible-static
  let slist list 100 100
  let slist2 list 100 100
  set slist [[-15.71 -12.27 108.46][-5.04 14.75 120.15][-4.95 2.24 204.09][4.08 -0.04 133.18][-7.03 4.36 29.13][4.51 8.03 6.09][-9.61 0.98 29.73][-15.24 -9.45 321.5][2.23 -12.05 139.95][-3.86 -2.9 231.51][-5.15 0.84 32.76][-0.09 -2.29 44.1][11.86 15.93 93.85][-4.37 -6.25 263.0][0.38 -4.87 54.79][-15.5 -2.78 88.43][-13.81 -2.5 122.31][7.99 3.02 288.28][5.84 -13.27 316.24][-9.46 -9.63 121.25][14.35 5.77 76.64][3.05 -9.17 341.89][-11.32 4.83 78.81][-12.82 -14.9 61.16][-6.98 -11.61 241.06][4.05 -2.45 111.65][1.78 -11.07 196.35][-15.46 -2.48 123.73][7.62 0.01 126.06][-1.02 12.38 228.98][-5.71 -2.5 336.81][-11.36 -10.79 336.1][11.8 6.7 334.11][-8.75 1.61 107.52][1.62 -11.15 67.27][8.84 15.0 317.26][9.11 13.1 265.6][6.51 15.98 181.26][-2.8 9.14 189.14][10.54 9.23 173.87][-4.38 -10.2 15.67][-10.84 -14.67 326.81][0.49 -8.06 357.55][6.95 6.65 356.99][-15.51 -6.4 53.75][5.47 3.69 170.61][4.41 12.1 49.04][-13.82 6.4 241.37][6.88 9.28 62.54][9.12 -14.1 299.58][-0.5 -9.55 228.46][4.22 -1.54 78.32][4.96 -5.79 197.63][10.9 -7.79 208.66][-3.13 -7.61 176.43][14.0 -14.23 101.82][9.89 -0.96 335.35][-10.56 -8.05 157.75][-14.68 -14.89 92.51][-3.47 -14.81 115.38][-11.94 12.92 255.05][14.98 -15.7 180.88][7.33 11.26 10.48][-0.17 6.6 123.83][-8.47 15.81 274.19][8.26 -5.09 63.39][-12.16 -13.2 117.49][8.94 0.34 40.98][1.45 -1.66 356.86][0.8 2.69 340.27][13.49 8.43 246.56][-2.92 2.92 52.14][-0.86 3.62 217.57][0.77 -4.04 256.26][1.5 -7.31 179.96][-5.08 10.01 237.96][0.38 -15.15 69.23][-3.25 -1.99 343.13][8.42 -11.05 354.3][-3.6 -12.59 43.28][1.88 -9.43 101.4][-12.76 -2.38 121.24][15.02 4.05 4.18][-7.29 -12.08 193.6][0.63 -4.0 18.12][9.57 -1.39 136.88][-3.68 -14.49 11.28][7.94 4.75 339.89][4.19 -14.34 81.89][-11.25 11.63 116.95][-3.49 -7.96 89.58][4.26 -7.82 185.0][-9.14 3.94 199.16][-13.03 4.07 119.89][12.54 8.21 200.2][-6.3 -15.95 43.02][2.91 -14.92 90.36][-7.43 12.46 113.11][-13.15 -3.38 94.44][11.77 0.69 124.7][11.77 0.69 124.7]]
  set slist2 sublist slist 1 (initial_susceptible + 1)
  foreach slist2
  [
    x -> create-susceptible 1
    [
      setxy (item 0 x) (item 1 x)
      set heading (item 2 x)
      set color orange
      set energy agent-starting-energy
    ]
  ]
end

to setup-infected-static
  let ilist list 100 100
  let ilist2 list 100 100
  set ilist [[-10.51 11.62 341.06][1.27 -6.06 256.73][4.25 12.83 87.79][2.75 -10.16 53.84][12.23 -14.35 120.98][-9.2 -13.55 236.41][2.5 11.78 205.72][-8.93 8.76 278.64][-13.33 14.23 112.9][-4.21 -12.29 259.83][1.18 1.68 298.94][13.99 2.9 43.83][-5.01 -9.1 314.84][-14.01 -8.01 151.24][-13.39 -0.74 288.91][-3.5 -12.25 95.25][1.58 1.02 354.34][5.48 -5.43 37.14][-8.42 12.57 242.31][-14.43 -14.25 109.0][-10.49 -12.69 184.08][-15.05 -9.13 169.64][-12.22 -6.71 273.32][-13.55 -10.63 188.69][-11.73 4.02 255.14][-7.98 13.06 258.91][8.31 -12.01 87.16][11.25 15.15 127.48][-14.16 -13.11 162.76][-12.74 -13.69 284.08][5.14 -14.05 131.85][13.76 1.38 112.51][1.16 15.86 310.06][-1.45 6.87 231.24][6.01 -13.17 174.9][9.04 4.82 70.23][0.3 8.67 226.96][0.57 -0.34 177.6][-15.88 5.2 194.15][7.8 -2.87 169.99][-11.78 1.16 42.96][6.12 -0.07 230.21][8.1 -15.37 203.69][-2.05 -7.96 268.46][-6.65 13.56 306.63][1.53 -6.33 3.92][8.23 -13.77 183.92][-13.97 5.02 244.71][14.41 13.23 314.21][-7.03 5.8 263.43][-9.95 -3.89 138.41][12.06 1.7 315.75][-14.79 -11.23 145.4][-8.61 -2.97 309.9][3.05 3.52 279.93][-5.83 5.36 329.4][-9.79 15.7 240.23][7.03 1.98 83.08][1.81 -7.85 239.16][-10.93 -15.97 265.17][-11.5 -9.15 70.57][5.02 1.04 109.01][8.5 1.07 75.97][1.67 5.76 355.09][15.25 -5.02 348.68][-7.53 -8.18 198.96][0.63 12.84 162.34][12.43 -10.31 48.88][-2.72 -7.22 178.77][15.05 4.13 67.63][15.99 7.89 163.01][3.93 2.71 192.98][12.51 3.06 122.91][-11.54 -11.22 206.61][-3.93 1.94 343.24][-12.33 5.45 154.84][-3.53 5.13 341.84][2.23 5.91 314.17][0.51 9.51 184.25][0.97 4.75 332.97][8.14 7.93 331.76][-3.61 -5.35 38.68][-12.89 0.43 355.66][-12.07 -14.29 342.45][2.47 14.74 96.63][0.25 -4.33 155.29][-6.99 4.35 213.77][-12.58 1.21 189.81][-10.02 9.45 355.64][6.2 2.66 335.13][2.85 7.41 106.31][-4.26 8.39 234.55][10.88 14.29 0.22][-13.3 3.22 60.05][-7.21 -11.85 38.93][-0.08 11.92 102.96][11.07 -5.73 165.49][14.21 -5.96 140.12][2.89 -13.77 273.98][-7.76 15.79 96.57][-7.76 15.79 96.57]]
  set ilist2 sublist ilist 1 (initial_infected + 1)
  foreach ilist2
  [
    x -> create-infected 1
    [
      setxy (item 0 x) (item 1 x)
      set heading (item 2 x)
      set color magenta
      set energy agent-starting-energy
    ]
  ]
end

to setup-exposed-static
  if Model = "SEIR" or Model = "SEIRS"
  [
    let elist list 100 100
    let elist2 list 100 100
    set elist [[6.07 6.65 22.23][13.44 14.16 351.44][-4.62 -5.47 86.79][0.08 -1.05 246.57][13.03 12.81 278.12][-7.69 7.19 357.28][1.71 8.01 290.37][2.59 -10.52 78.64][-0.24 8.01 176.59][1.34 -11.15 190.45][11.31 9.06 30.18][2.47 8.79 261.19][-13.69 -15.72 98.84][1.97 -9.23 286.38][-5.7 9.86 81.33][-13.57 -13.45 82.52][-9.55 14.59 254.29][-11.99 12.59 271.37][-1.93 -1.9 124.56][12.33 8.37 150.74][-3.21 7.37 273.14][13.28 11.16 163.17][-7.31 -0.9 79.62][10.12 -8.7 55.7][14.28 -2.56 121.1][15.38 -15.24 313.51][-6.34 -0.99 122.43][-6.43 -3.84 180.33][10.75 15.28 160.62][-6.91 -14.64 16.11][-0.91 4.48 291.91][-15.18 11.06 38.56][-5.93 -15.33 192.17][2.9 2.47 234.86][-0.22 -10.92 38.94][-10.39 11.69 130.89][1.77 10.69 37.89][-3.89 8.35 159.95][-2.36 -3.5 304.96][10.63 13.13 304.99][2.8 2.51 184.51][-0.79 15.67 8.03][-10.86 -0.28 254.47][9.0 -11.54 254.6][-5.48 1.73 181.01][12.3 -7.33 282.36][-15.42 3.57 126.77][3.35 -8.72 307.45][0.78 -4.28 61.8][0.44 8.98 64.88][8.62 -6.98 4.26][15.34 -10.31 126.82][13.8 -8.9 211.19][15.31 9.46 41.24][-2.23 -7.32 85.42][15.01 9.81 149.86][-15.21 -8.31 100.02][-0.58 -2.01 354.84][0.48 -7.46 318.98][3.16 1.93 34.78][15.54 14.47 181.83][-5.36 6.87 310.96][-10.89 -9.12 242.99][13.8 5.17 71.94][-14.6 1.69 10.44][15.04 -4.62 318.3][-1.94 7.02 75.13][4.44 -13.87 165.89][-14.85 -15.11 273.57][-8.91 -3.41 291.77][10.15 -4.23 49.73][-12.8 -14.55 131.82][4.31 15.61 293.6][-1.38 11.42 1.78][12.3 13.07 153.98][2.58 -0.45 247.99][-6.41 7.16 264.46][14.91 13.18 26.08][-3.33 13.25 172.93][-9.14 10.5 57.57][10.1 -4.45 190.16][-7.0 -13.54 82.83][6.65 -10.06 207.06][-6.0 -15.73 124.63][-8.53 -2.84 355.64][13.11 3.82 29.69][-13.05 -6.88 58.48][9.1 -10.31 155.89][-13.38 -7.9 1.81][-12.37 -9.54 290.94][-9.08 -3.41 67.77][-7.13 10.21 75.31][2.83 13.99 58.76][-9.62 -4.4 143.8][8.58 10.82 119.03][6.24 10.14 85.01][-0.01 9.7 60.23][0.32 -7.73 208.57][12.36 -1.18 97.22][9.58 -15.22 106.24][9.58 -15.22 106.24]]
    set elist2 sublist elist 1 (initial_exposed + 1)
    foreach elist2
    [
      x -> create-exposed 1
      [
        setxy (item 0 x) (item 1 x)
        set heading (item 2 x)
        set color violet
        set energy agent-starting-energy
      ]
    ]
  ]
end

to setup-immune-static
  if Model = "SIR" or Model = "SIRS" or Model = "SEIR" or Model = "SEIRS"
  [
    let rlist list 100 100
    let rlist2 list 100 100
    set rlist [[-3.54 1.75 169.52][0.25 -4.44 275.01][-11.46 1.53 289.95][-9.19 -7.25 242.02][-1.3 10.66 313.32][3.92 -3.34 342.4][12.29 -0.59 123.5][-12.49 -6.62 133.4][11.89 -7.37 185.7][13.48 -7.12 225.3][-9.67 6.59 83.11][-1.11 -7.02 202.71][-6.19 3.02 309.98][14.77 7.46 356.9][-10.14 -3.94 61.0][2.58 1.84 54.39][-13.78 9.82 116.32][4.4 -4.96 212.02][10.4 -0.85 189.96][2.07 0.75 172.26][0.86 15.03 142.84][-5.64 -2.46 80.35][-1.27 4.75 124.23][-0.5 12.39 356.09][7.12 -11.69 218.64][-11.83 3.96 338.71][-1.85 -5.38 179.75][11.84 -13.59 267.22][1.73 6.78 316.58][-6.19 -12.7 344.93][-6.42 4.31 150.89][-9.87 -14.88 89.69][-13.22 -11.86 105.59][-15.65 2.59 116.61][-14.65 -5.46 345.84][-12.58 0.24 98.56][-1.55 5.69 253.5][-5.48 0.56 157.6][10.05 11.37 324.37][5.49 -6.73 1.44][5.55 8.0 358.66][-0.17 2.7 292.23][4.01 6.82 187.53][-4.03 7.56 162.41][4.74 11.95 325.27][1.58 -8.94 1.8][13.91 -5.87 308.86][1.3 9.42 52.28][-6.38 6.88 302.98][11.81 8.52 210.66][-9.18 -9.76 38.58][-0.45 3.35 304.38][-12.11 1.4 113.17][-4.81 -13.03 220.89][-5.77 -5.69 156.16][-14.11 15.62 303.33][-2.38 0.27 297.12][2.06 -12.92 200.05][9.42 -9.26 41.4][-9.26 13.47 300.3][-12.4 -10.86 344.48][7.11 12.47 293.1][12.41 7.02 309.49][-15.61 -1.65 117.08][5.01 0.1 209.01][-14.53 -10.67 229.54][15.42 -11.39 236.53][2.27 13.18 96.19][4.18 -1.38 250.28][-11.7 -2.01 227.19][-5.7 -2.15 251.54][-14.02 -15.66 134.49][-1.97 11.04 4.25][10.93 -1.71 78.18][11.84 7.1 1.41][12.04 15.89 48.49][-3.8 -5.01 302.11][11.82 9.3 19.33][-5.74 4.17 171.95][-8.76 13.44 127.12][7.48 3.3 200.11][-4.41 8.72 304.22][-14.4 -7.06 339.57][-1.45 8.96 137.47][11.7 -12.28 303.29][3.21 -2.82 92.94][5.08 14.78 170.85][-15.75 -3.92 192.24][7.95 3.09 254.64][4.84 6.31 324.34][-4.39 -15.55 209.32][14.63 -3.84 117.39][-9.88 -4.63 295.89][5.39 15.02 262.57][14.25 -10.55 278.71][-10.62 -15.16 233.45][5.68 0.3 166.28][8.3 -5.34 261.3][-9.52 1.31 22.51][3.12 -12.4 109.05]]
    set rlist2 sublist rlist 1 (initial_immune + 1)
    foreach rlist2
    [
      x -> create-immune 1
      [
        setxy (item 0 x) (item 1 x)
        set heading (item 2 x)
        set color sky
        set energy agent-starting-energy
      ]
    ]
  ]
end



to setup-patches
  ask patches
  [
    set information (((pxcor + pycor) * 25 + pxcor * 95 + pycor * 55 + 25) mod 100)
    set pcolor 57 - 5 * information / 100
  ]
  if misinfo-upper-left? [zombie-grass-ul]
  if misinfo-upper-right? [zombie-grass-ur]
  if misinfo-lower-left? [zombie-grass-ll]
  if misinfo-lower-right? [zombie-grass-lr]
end


to zombie-grass-ul
  ask patches with [pxcor = min-pxcor / 2 and pycor = max-pycor / 2]
  [ set pcolor red ]
end

to zombie-grass-ur
  ask one-of patches with [pxcor = max-pxcor / 2 and pycor = max-pycor / 2]
  [ set pcolor red ]
end

to zombie-grass-ll
  ask one-of patches with [pxcor = min-pxcor / 2 and pycor = min-pycor / 2]
  [ set pcolor red ]
end

to zombie-grass-lr
  ask one-of patches with [pxcor = max-pxcor / 2 and pycor = min-pycor / 2]
  [ set pcolor red ]
end

to go
  move-turtles
  ;feed-turtles
  feed-exposed
  feed-immune
  feed-susceptible
  feed-infected
  reproduce-susceptible
  ;reproduce-infected
  heal-infected
  spread-misinfo
  become-infected
  immunity-loss
  grow-grass
  death
  tick
  if ticks > max-ticks and stop-after? [stop]
end


to move-turtles
  ask turtles
  [
    carefully
    [
      let target max-one-of patches in-cone 4 60 [information]
      let target-backup max-one-of patches in-radius 4 [information]
      ifelse target != nobody and target != patch-here
      [
        set heading towards target
      ]
      [
        set heading towards target-backup
      ]
    ]
    [ ]

    forward 1
    set energy energy - agent-loss-move
  ]
end

;to feed-turtles
;  ask turtles
;  [
;    set total_information sum [information] of patches
;    if information >= 10
;    [
;      set energy (energy + rho / information)
;      set information (information - rho / information)
;    ]
;  ]
;end

to feed-exposed
  ask exposed
  [
    if pcolor != red
    [
      if information >= 10
      [
        set energy energy + 0.1 * 100 ; rho = 0.1
        set information (information - 10)
      ]
    ]
    if pcolor = red
    [
      set breed infected
      set color magenta
    ]
  ]
end

to feed-immune
  ask immune
  [
    if pcolor != red
    [
      if information >= 10
      [
        set energy energy + 0.1 * 100
        set information (information - 10)
      ]
    ]
    if pcolor = red
    [
      set breed infected
      set color magenta
    ]
  ]
end


to feed-susceptible
  ask susceptible
  [
    if pcolor != red
    [
      if information >= 10
      [
        set energy energy + 0.1 * 100
        set information (information - 10)
      ]
    ]
    if pcolor = red
    [
      set breed infected
      set color magenta
    ]
  ]
end

to feed-infected
ask infected
[
    if pcolor != red
    [
      if information >= 10
      [
        set energy energy + 0.1 * 100
        set information (information - 10)
      ]
    ]
    if pcolor = red
    [
      set energy energy + 0.1 * 100
    ]
]
end

to reproduce-susceptible
  create-susceptible ((count turtles) * 0.00)
  [
      ;set x random 30
      ;set y random 30
      ;set z random 360
      setxy ((random 30) - 15) ((random 30) - 15)
      set heading (random 360)
      set color orange
      set energy agent-starting-energy
  ]

end

to reproduce-infected
  create-infected ((count turtles) * 0.00 / 100)
  [
      ;set x random 30
      ;set y random 30
      ;set z random 360
      setxy ((random 30) - 15) ((random 30) - 15)
      set heading (random 360)
      set color orange
      set energy agent-starting-energy
  ]
end

to spread-misinfo
  ask infected
  [
    if count susceptible-here > 0
    [
      carefully[
        let closest-susceptible min-one-of susceptible-here [distance myself]
        if random 1000 < beta * 1000 * 2 * count(patches) / count(susceptible)
        [
          ifelse Model = "SEIR" or Model = "SEIRS"
          [
            ask closest-susceptible [set breed exposed set color violet]
          ]
          [
            ask closest-susceptible [set breed infected set color magenta]
          ]
        ]
      ][ ]
    ]
  ]
end

to become-infected
  ask exposed
  [
    carefully[
      if random 1000 < sigma * 1000
      [
        set breed infected set color magenta
      ]
    ][ ]
  ]
end

to heal-infected
  ask infected
  [
    (ifelse Model = "SI"
    [
      ;do nothing
    ]
    Model = "SIS"
    [
      if random 1000 < gamma * 1000
      [
        set breed susceptible set color orange
      ]
    ]
    Model = "SIR" or Model = "SIRS" or Model = "SEIR" or Model = "SEIRS"
    [
      if random 1000 < gamma * 1000
      [
        set breed immune set color sky
      ]
    ]
    [
      ;error - invalid model
    ])


  ]
end


to immunity-loss
  ask immune
  [
    if Model = "SIRS" or Model = "SEIRS"
    [
      if random 1000 < xi * 1000
      [
        set breed susceptible set color orange
      ]
    ]
  ]
end





to grow-grass
  ask patches
  [
    if pcolor != red
    [
      if information < 100
      [
        set information (information + info-regrowth-rate * 100)
      ]
      set pcolor 59.5 - 7.5 * information / 100 ; rescaling information: [0 , 100] to [57 , 52]
    ]
  ]

end

to death
  ask turtles with [energy <= 0]
  [
    die
  ]
end
@#$#@#$#@
GRAPHICS-WINDOW
340
10
859
530
-1
-1
15.5
1
10
1
1
1
0
1
1
1
-16
16
-16
16
1
1
1
ticks
30.0

BUTTON
3
10
83
43
NIL
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
85
10
148
43
NIL
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

PLOT
861
57
1321
203
number of agents
time
agents
0.0
10.0
0.0
10.0
true
true
"" ""
PENS
"susceptible" 1.0 0 -955883 true "" "plot count susceptible"
"infected" 1.0 0 -5825686 true "" "plot count infected"
"recovered" 1.0 0 -13791810 true "" "plot count immune"
"exposed" 1.0 0 -8630108 true "" "plot count exposed"

PLOT
861
205
1321
355
total amount of information
NIL
NIL
0.0
10.0
0.0
10.0
true
true
"" ""
PENS
"total information" 1.0 0 -10899396 true "" "plot sum [information] of patches"

SWITCH
5
105
110
138
stop-after?
stop-after?
0
1
-1000

INPUTBOX
5
45
110
105
max-ticks
200.0
1
0
Number

SLIDER
5
227
171
260
agent-loss-move
agent-loss-move
0
10
2.0
1
1
NIL
HORIZONTAL

SWITCH
5
260
171
293
misinfo-upper-left?
misinfo-upper-left?
1
1
-1000

SWITCH
172
260
340
293
misinfo-upper-right?
misinfo-upper-right?
1
1
-1000

SWITCH
5
294
171
327
misinfo-lower-left?
misinfo-lower-left?
1
1
-1000

SWITCH
172
294
340
327
misinfo-lower-right?
misinfo-lower-right?
1
1
-1000

SLIDER
5
347
340
380
beta
beta
0
1
0.2
0.001
1
NIL
HORIZONTAL

SLIDER
5
397
340
430
gamma
gamma
0
1
0.03
0.001
1
NIL
HORIZONTAL

SLIDER
5
447
340
480
sigma
sigma
0
1
0.155
0.001
1
NIL
HORIZONTAL

SLIDER
5
497
340
530
xi
xi
0
1
0.001
0.001
1
NIL
HORIZONTAL

CHOOSER
150
10
338
55
Model
Model
"SI" "SIS" "SIR" "SIRS" "SEIR" "SEIRS"
5

TEXTBOX
10
330
160
348
Infectious rate (beta):
11
0.0
1

TEXTBOX
10
380
160
398
Recovery rate (gamma):
11
0.0
1

TEXTBOX
10
480
160
498
Immunity loss rate (xi):
11
0.0
1

TEXTBOX
10
430
160
448
Incubation rate (sigma):
11
0.0
1

SLIDER
113
56
339
89
initial_susceptible
initial_susceptible
1
100
100.0
1
1
NIL
HORIZONTAL

SLIDER
113
90
339
123
initial_infected
initial_infected
0
100
50.0
1
1
NIL
HORIZONTAL

MONITOR
1155
10
1322
55
Total Amount of Information
sum [information] of patches
17
1
11

MONITOR
1011
10
1153
55
Total Number of Agents
count turtles
17
1
11

MONITOR
862
10
1009
55
Total Number of Patches
count patches
17
1
11

SLIDER
114
125
339
158
initial_exposed
initial_exposed
0
100
0.0
1
1
NIL
HORIZONTAL

SLIDER
114
159
339
192
initial_immune
initial_immune
0
100
0.0
1
1
NIL
HORIZONTAL

SLIDER
172
227
340
260
agent-starting-energy
agent-starting-energy
0
100
50.0
1
1
NIL
HORIZONTAL

SLIDER
5
193
339
226
info-regrowth-rate
info-regrowth-rate
0
1
0.03
0.01
1
NIL
HORIZONTAL

@#$#@#$#@
## WHAT IS IT?

(a general understanding of what the model is trying to show or explain)

## HOW IT WORKS

(what rules the agents use to create the overall behavior of the model)

## HOW TO USE IT

(how to use the model, including a description of each of the items in the Interface tab)

## THINGS TO NOTICE

(suggested things for the user to notice while running the model)

## THINGS TO TRY

(suggested things for the user to try to do (move sliders, switches, etc.) with the model)

## EXTENDING THE MODEL

(suggested things to add or change in the Code tab to make the model more complicated, detailed, accurate, etc.)

## NETLOGO FEATURES

(interesting or unusual features of NetLogo that the model uses, particularly in the Code tab; or where workarounds were needed for missing features)

## RELATED MODELS

(models in the NetLogo Models Library and elsewhere which are of related interest)

## CREDITS AND REFERENCES

(a reference to the model's URL on the web if it has one, as well as any other necessary credits, citations, and links)
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.3.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
<experiments>
  <experiment name="SI" repetitions="1000" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>count turtles</metric>
    <metric>count susceptible</metric>
    <metric>count infected</metric>
    <metric>count exposed</metric>
    <metric>count immune</metric>
    <metric>run-seed</metric>
    <enumeratedValueSet variable="sigma">
      <value value="0.155"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="gamma">
      <value value="0.03"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="agent-loss-move">
      <value value="2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_immune">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-upper-right?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="beta">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-lower-left?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_infected">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-lower-right?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_susceptible">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="max-ticks">
      <value value="200"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_exposed">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-upper-left?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Model">
      <value value="&quot;SI&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="agent-starting-energy">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="info-regrowth-rate">
      <value value="0.03"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="xi">
      <value value="0.001"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="stop-after?">
      <value value="true"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="SIS" repetitions="1000" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>count turtles</metric>
    <metric>count susceptible</metric>
    <metric>count infected</metric>
    <metric>count exposed</metric>
    <metric>count immune</metric>
    <metric>run-seed</metric>
    <enumeratedValueSet variable="sigma">
      <value value="0.155"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="gamma">
      <value value="0.03"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="agent-loss-move">
      <value value="2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_immune">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-upper-right?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="beta">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-lower-left?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_infected">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-lower-right?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_susceptible">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="max-ticks">
      <value value="200"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_exposed">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-upper-left?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Model">
      <value value="&quot;SIS&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="agent-starting-energy">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="info-regrowth-rate">
      <value value="0.03"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="xi">
      <value value="0.001"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="stop-after?">
      <value value="true"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="SIR" repetitions="1000" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>count turtles</metric>
    <metric>count susceptible</metric>
    <metric>count infected</metric>
    <metric>count exposed</metric>
    <metric>count immune</metric>
    <metric>run-seed</metric>
    <enumeratedValueSet variable="sigma">
      <value value="0.155"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="gamma">
      <value value="0.03"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="agent-loss-move">
      <value value="2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_immune">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-upper-right?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="beta">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-lower-left?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_infected">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-lower-right?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_susceptible">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="max-ticks">
      <value value="200"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_exposed">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-upper-left?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Model">
      <value value="&quot;SIR&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="agent-starting-energy">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="info-regrowth-rate">
      <value value="0.03"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="xi">
      <value value="0.001"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="stop-after?">
      <value value="true"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="SIRS" repetitions="1000" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>count turtles</metric>
    <metric>count susceptible</metric>
    <metric>count infected</metric>
    <metric>count exposed</metric>
    <metric>count immune</metric>
    <metric>run-seed</metric>
    <enumeratedValueSet variable="sigma">
      <value value="0.155"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="gamma">
      <value value="0.03"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="agent-loss-move">
      <value value="2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_immune">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-upper-right?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="beta">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-lower-left?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_infected">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-lower-right?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_susceptible">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="max-ticks">
      <value value="200"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_exposed">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-upper-left?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Model">
      <value value="&quot;SIRS&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="agent-starting-energy">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="info-regrowth-rate">
      <value value="0.03"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="xi">
      <value value="0.001"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="stop-after?">
      <value value="true"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="SEIR" repetitions="1000" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>count turtles</metric>
    <metric>count susceptible</metric>
    <metric>count infected</metric>
    <metric>count exposed</metric>
    <metric>count immune</metric>
    <metric>run-seed</metric>
    <enumeratedValueSet variable="sigma">
      <value value="0.155"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="gamma">
      <value value="0.03"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="agent-loss-move">
      <value value="2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_immune">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-upper-right?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="beta">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-lower-left?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_infected">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-lower-right?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_susceptible">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="max-ticks">
      <value value="200"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_exposed">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-upper-left?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Model">
      <value value="&quot;SEIR&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="agent-starting-energy">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="info-regrowth-rate">
      <value value="0.03"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="xi">
      <value value="0.001"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="stop-after?">
      <value value="true"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="SEIRS" repetitions="1000" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>count turtles</metric>
    <metric>count susceptible</metric>
    <metric>count infected</metric>
    <metric>count exposed</metric>
    <metric>count immune</metric>
    <metric>run-seed</metric>
    <enumeratedValueSet variable="sigma">
      <value value="0.155"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="gamma">
      <value value="0.03"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="agent-loss-move">
      <value value="2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_immune">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-upper-right?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="beta">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-lower-left?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_infected">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-lower-right?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_susceptible">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="max-ticks">
      <value value="200"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial_exposed">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="misinfo-upper-left?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Model">
      <value value="&quot;SEIRS&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="agent-starting-energy">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="info-regrowth-rate">
      <value value="0.03"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="xi">
      <value value="0.001"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="stop-after?">
      <value value="true"/>
    </enumeratedValueSet>
  </experiment>
</experiments>
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
1
@#$#@#$#@
