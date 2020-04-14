
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
import knot from 'knot.js'

const bricks = (options = {}) => {
  // privates

  let persist           // packing new elements, or all elements?
  let ticking           // for debounced resize

  let sizeIndex
  let sizeDetail

  let columnTarget
  let columnHeights

  let nodeTop
  let nodeLeft
  let nodeWidth
  let nodeHeight

  let nodes
  let nodesWidths
  let nodesHeights

  // resolve options

  const packed = options.packed.indexOf('data-') === 0 ? options.packed : `data-${options.packed}`
  const sizes = options.sizes.slice().reverse()
  const position = options.position !== false

  const container = options.container.nodeType
    ? options.container
    : document.querySelector(options.container)

  const selectors = {
    all: () => toArray(container.children),
    new: () => toArray(container.children).filter(node => !node.hasAttribute(`${packed}`))
  }

  // series

  const setup = [
    setSizeIndex,
    setSizeDetail,
    setColumns
  ]

  const run = [
    setNodes,
    setNodesDimensions,
    setNodesStyles,
    setContainerStyles
  ]

  // instance

  const instance = knot({
    pack,
    update,
    resize
  })

  return instance

  // general helpers

  function runSeries (functions) {
    functions.forEach(func => func())
  }

  // array helpers

  function toArray (input, scope = document) {
    return Array.prototype.slice.call(input)
  }

  function fillArray (length) {
    return Array.apply(null, Array(length)).map(() => 0)
  }

  // size helpers

  function getSizeIndex () {
    // find index of widest matching media query
    return sizes
      .map(size => size.mq && window.matchMedia(`(min-width: ${size.mq})`).matches)
      .indexOf(true)
  }

  function setSizeIndex () {
    sizeIndex = getSizeIndex()
  }

  function setSizeDetail () {
    // if no media queries matched, use the base case
    sizeDetail = sizeIndex === -1
      ? sizes[sizes.length - 1]
      : sizes[sizeIndex]
  }

  // column helpers

  function setColumns () {
    columnHeights = fillArray(sizeDetail.columns)
  }

  // node helpers

  function setNodes () {
    nodes = selectors[persist ? 'new' : 'all']()
  }

  function setNodesDimensions () {
    // exit if empty container
    if (nodes.length === 0) {
      return
    }

    nodesWidths = nodes.map(element => element.clientWidth)
    nodesHeights = nodes.map(element => element.clientHeight)
  }

  function setNodesStyles () {
    nodes.forEach((element, index) => {
      columnTarget = columnHeights.indexOf(Math.min.apply(Math, columnHeights))

      element.style.position = 'absolute'

      nodeTop = `${columnHeights[columnTarget]}px`
      nodeLeft = `${(columnTarget * nodesWidths[index]) + (columnTarget * sizeDetail.gutter)}px`

      // support positioned elements (default) or transformed elements
      if (position) {
        element.style.top = nodeTop
        element.style.left = nodeLeft
      } else {
        element.style.transform = `translate3d(${nodeLeft}, ${nodeTop}, 0)`
      }

      element.setAttribute(packed, '')

      // ignore nodes with no width and/or height
      nodeWidth = nodesWidths[index]
      nodeHeight = nodesHeights[index]

      if (nodeWidth && nodeHeight) {
        columnHeights[columnTarget] += nodeHeight + sizeDetail.gutter
      }
    })
  }

  // container helpers

  function setContainerStyles () {
    container.style.position = 'relative'
    container.style.width = `${sizeDetail.columns * nodeWidth + (sizeDetail.columns - 1) * sizeDetail.gutter}px`
    container.style.height = `${Math.max.apply(Math, columnHeights) - sizeDetail.gutter}px`
  }

  // resize helpers

  function resizeFrame () {
    if (!ticking) {
      window.requestAnimationFrame(resizeHandler)
      ticking = true
    }
  }

  function resizeHandler () {
    if (sizeIndex !== getSizeIndex()) {
      pack()
      instance.emit('resize', sizeDetail)
    }

    ticking = false
  }

  // API

  function pack () {
    persist = false
    runSeries(setup.concat(run))

    return instance.emit('pack')
  }

  function update () {
    persist = true
    runSeries(run)

    return instance.emit('update')
  }

  function resize (flag = true) {
    const action = flag
      ? 'addEventListener'
      : 'removeEventListener'

    window[action]('resize', resizeFrame)

    return instance
  }
}

export default bricks
