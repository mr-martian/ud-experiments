#!/usr/bin/env python3

import itertools

common_content = '''
<section-def-vars>
  <def-var n="tag_param"/>
  <def-var n="trace_surface"/>
  <def-var n="chunk_surface"/>
  <def-var n="trace_tag"/>
  <def-var n="head_tag"/>
  <def-var n="dep_tag"/>
</section-def-vars>
<section-def-macros>
  <def-macro n="negate" npar="1">
    <choose><when><test>
      <contains-substring>
        <clip pos="1" side="tl" part="tags"/>
        <var n="tag_param"/>
      </contains-substring>
    </test>
      <reject-current-rule/>
    </when></choose>
  </def-macro>
  <def-macro n="get_chunk" npar="1">
    <choose>
      <when>
        <test>
          <equal><clip pos="1" side="sl" part="whole"/><lit v=""/></equal>
        </test>
        <let>
          <var n="chunk_surface"/>
          <clip pos="1" side="tl" part="whole"/>
        </let>
      </when>
      <otherwise>
        <let>
          <var n="chunk_surface"/>
          <clip pos="1" side="sl" part="whole"/>
        </let>
      </otherwise>
    </choose>
  </def-macro>
  <def-macro n="out_plain" npar="1">
    <choose>
      <when>
        <test>
          <not>
            <equal>
              <clip pos="1" side="sl" part="whole"/>
              <lit v=""/>
            </equal>
          </not>
        </test>
        <out>
          <chunk>
            <target>
              <clip pos="1" side="sl" part="whole"/>
            </target>
            <contents>
              <chunk>
                <source><clip pos="1" side="sl" part="whole"/></source>
                <target><clip pos="1" side="tl" part="whole"/></target>
                <reference><clip pos="1" side="ref" part="whole"/></reference>
              </chunk>
            </contents>
          </chunk>
        </out>
      </when>
      <otherwise>
        <out>
          <lu><clip pos="1" side="tl" part="whole"/></lu>
        </out>
      </otherwise>
    </choose>
  </def-macro>
  <def-macro n="get_trace" npar="1">
    <choose>
      <when>
        <test>
          <not>
            <equal>
              <clip pos="1" side="sl" part="whole"/>
              <lit v=""/>
            </equal>
          </not>
        </test>
        <let><var n="trace_surface"/><clip pos="1" side="sl" part="whole"/></let>
      </when>
      <otherwise>
        <let><var n="trace_surface"/><clip pos="1" side="tl" part="whole"/></let>
      </otherwise>
    </choose>
    <append n="trace_surface"><lit-tag v="@trace"/></append>
    <let><var n="trace_tag"/><lit-tav v="@@trace"/></let>
  </def-macro>
  <def-macro n="out_trace_left" npar="2">
    <call-macro n="get_trace"><with-param pos="2"/></call-macro>
    <choose>
      <when>
        <test>
          <not>
            <equal>
              <clip pos="1" side="sl" part="whole"/>
              <lit v=""/>
            </equal>
          </not>
        </test>
        <out>
          <chunk>
            <target>
              <clip pos="1" side="sl" part="whole"/>
            </target>
            <contents>
              <lu><var n="trace_surface"/></lu>
              <b/>
              <chunk>
                <source><clip pos="1" side="sl" part="whole"/></source>
                <target><clip pos="1" side="tl" part="whole"/></target>
                <reference><clip pos="1" side="ref" part="whole"/></reference>
              </chunk>
            </contents>
          </chunk>
        </out>
      </when>
      <otherwise>
        <out>
          <chunk>
            <target><clip pos="1" side="tl" part="whole"/></target>
            <contents>
              <lu><var n="trace_surface"/></lu>
              <b/>
              <lu><clip pos="1" side="tl" part="whole"/></lu>
            </contents>
          </chunk>
        </out>
      </otherwise>
    </choose>
  </def-macro>
  <def-macro n="out_trace_right" npar="1">
    <call-macro n="get_trace"><with-param pos="2"/></call-macro>
    <choose>
      <when>
        <test>
          <not>
            <equal>
              <clip pos="1" side="sl" part="whole"/>
              <lit v=""/>
            </equal>
          </not>
        </test>
        <out>
          <chunk>
            <target>
              <clip pos="1" side="sl" part="whole"/>
            </target>
            <contents>
              <chunk>
                <source><clip pos="1" side="sl" part="whole"/></source>
                <target><clip pos="1" side="tl" part="whole"/></target>
                <reference><clip pos="1" side="ref" part="whole"/></reference>
              </chunk>
              <b/>
              <lu><var n="trace_surface"/></lu>
            </contents>
          </chunk>
        </out>
      </when>
      <otherwise>
        <out>
          <chunk>
            <target><clip pos="1" side="tl" part="whole"/></target>
            <contents>
              <lu><clip pos="1" side="tl" part="whole"/></lu>
              <b/>
              <lu><var n="trace_surface"/></lu>
            </contents>
          </chunk>
        </out>
      </otherwise>
    </choose>
  </def-macro>
  <def-macro n="out_dep_left" npar="2">
    <choose>
      <when>
        <test><and>
          <not><equal><clip pos="1" side="sl" part="whole"/><lit v=""/></equal></not>
          <not><equal><clip pos="2" side="sl" part="whole"/><lit v=""/></equal></not>
        </and></test>
        <out>
          <chunk>
            <target>
              <clip pos="1" side="sl" part="whole"/>
              <var n="head_tag"/>
            </target>
            <contents>
              <chunk>
                <target>
                  <clip pos="2" side="sl" part="whole"/>
                  <var n="dep_tag"/>
                </target>
                <contents>
                  <chunk>
                    <source><clip pos="2" side="sl" part="whole"/></source>
                    <target><clip pos="2" side="tl" part="whole"/></target>
                    <reference><clip pos="2" side="ref" part="whole"/></reference>
                  </chunk>
                </contents>
              </chunk>
              <b/>
              <chunk>
                <source><clip pos="1" side="sl" part="whole"/></source>
                <target><clip pos="1" side="tl" part="whole"/></target>
                <reference><clip pos="1" side="ref" part="whole"/></reference>
              </chunk>
            </contents>
          </chunk>
        </out>
      </when>
      <when>
        <test><and>
          <not><equal><clip pos="1" side="sl" part="whole"/><lit v=""/></equal></not>
          <equal><clip pos="2" side="sl" part="whole"/><lit v=""/></equal>
        </and></test>
        <out>
          <chunk>
            <target>
              <clip pos="1" side="sl" part="whole"/>
              <var n="head_tag"/>
            </target>
            <contents>
              <lu><clip pos="2" side="tl" part="whole"/><var n="dep_tag"/></lu>
              <b/>
              <chunk>
                <source><clip pos="1" side="sl" part="whole"/></source>
                <target><clip pos="1" side="tl" part="whole"/></target>
                <reference><clip pos="1" side="ref" part="whole"/></reference>
              </chunk>
            </contents>
          </chunk>
        </out>
      </when>
      <when>
        <test><and>
          <equal><clip pos="1" side="sl" part="whole"/><lit v=""/></equal>
          <not><equal><clip pos="2" side="sl" part="whole"/><lit v=""/></equal></not>
        </and></test>
        <out>
          <chunk>
            <target>
              <clip pos="1" side="tl" part="whole"/>
              <var n="head_tag"/>
            </target>
            <contents>
              <chunk>
                <target>
                  <clip pos="2" side="tl" part="whole"/>
                  <var n="dep_tag"/>
                </target>
                <contents>
                  <chunk>
                    <source><clip pos="2" side="sl" part="whole"/></source>
                    <target><clip pos="2" side="tl" part="whole"/></target>
                    <reference><clip pos="2" side="ref" part="whole"/></reference>
                  </chunk>
                </contents>
              </chunk>
              <b/>
              <lu><clip pos="1" side="tl" part="whole"/></lu>
            </contents>
          </chunk>
        </out>
      </when>
      <otherwise>
        <out>
          <chunk>
            <target>
              <clip pos="1" side="tl" part="whole"/>
              <var n="head_tag"/>
            </target>
            <contents>
              <lu>
                <clip pos="2" side="tl" part="whole"/>
                <var n="dep_tag"/>
              </lu>
              <b/>
              <lu><clip pos="1" side="tl" part="whole"/></lu>
            </contents>
          </chunk>
        </out>
      </otherwise>
    </choose>
  </def-macro>
  <def-macro n="out_dep_right" npar="2">
    <choose>
      <when>
        <test><and>
          <not><equal><clip pos="1" side="sl" part="whole"/><lit v=""/></equal></not>
          <not><equal><clip pos="2" side="sl" part="whole"/><lit v=""/></equal></not>
        </and></test>
        <out>
          <chunk>
            <target>
              <clip pos="1" side="sl" part="whole"/>
              <var n="head_tag"/>
            </target>
            <contents>
              <chunk>
                <source><clip pos="1" side="sl" part="whole"/></source>
                <target><clip pos="1" side="tl" part="whole"/></target>
                <reference><clip pos="1" side="ref" part="whole"/></reference>
              </chunk>
              <b/>
              <chunk>
                <target>
                  <clip pos="2" side="sl" part="whole"/>
                  <var n="dep_tag"/>
                </target>
                <contents>
                  <chunk>
                    <source><clip pos="2" side="sl" part="whole"/></source>
                    <target><clip pos="2" side="tl" part="whole"/></target>
                    <reference><clip pos="2" side="ref" part="whole"/></reference>
                  </chunk>
                </contents>
              </chunk>
            </contents>
          </chunk>
        </out>
      </when>
      <when>
        <test><and>
          <not><equal><clip pos="1" side="sl" part="whole"/><lit v=""/></equal></not>
          <equal><clip pos="2" side="sl" part="whole"/><lit v=""/></equal>
        </and></test>
        <out>
          <chunk>
            <target>
              <clip pos="1" side="sl" part="whole"/>
              <var n="head_tag"/>
            </target>
            <contents>
              <chunk>
                <source><clip pos="1" side="sl" part="whole"/></source>
                <target><clip pos="1" side="tl" part="whole"/></target>
                <reference><clip pos="1" side="ref" part="whole"/></reference>
              </chunk>
              <b/>
              <lu><clip pos="2" side="tl" part="whole"/><var n="dep_tag"/></lu>
            </contents>
          </chunk>
        </out>
      </when>
      <when>
        <test><and>
          <equal><clip pos="1" side="sl" part="whole"/><lit v=""/></equal>
          <not><equal><clip pos="2" side="sl" part="whole"/><lit v=""/></equal></not>
        </and></test>
        <out>
          <chunk>
            <target>
              <clip pos="1" side="tl" part="whole"/>
              <var n="head_tag"/>
            </target>
            <contents>
              <lu><clip pos="1" side="tl" part="whole"/></lu>
              <b/>
              <chunk>
                <target>
                  <clip pos="2" side="tl" part="whole"/>
                  <var n="dep_tag"/>
                </target>
                <contents>
                  <chunk>
                    <source><clip pos="2" side="sl" part="whole"/></source>
                    <target><clip pos="2" side="tl" part="whole"/></target>
                    <reference><clip pos="2" side="ref" part="whole"/></reference>
                  </chunk>
                </contents>
              </chunk>
            </contents>
          </chunk>
        </out>
      </when>
      <otherwise>
        <out>
          <chunk>
            <target>
              <clip pos="1" side="tl" part="whole"/>
              <var n="head_tag"/>
            </target>
            <contents>
              <lu><clip pos="1" side="tl" part="whole"/></lu>
              <b/>
              <lu>
                <clip pos="2" side="tl" part="whole"/>
                <var n="dep_tag"/>
              </lu>
            </contents>
          </chunk>
        </out>
      </otherwise>
    </choose>
  </def-macro>
</section-def-macros>
'''

class Rule:
    def __init__(self, ruleid, pattern, head, dep, rel):
        self.ruleid = ruleid
        self.pattern = pattern
        self.head = head
        self.dep = dep
        self.rel = rel
    def get_patterns(self):
        ret = ''
        for i, p in enumerate(self.pattern):
            ct = '<def-cat n="%s_%s">' % (self.ruleid, i)
            ls = p.split('.')
            tags = '.'.join(x for x in ls if '@@' not in x)
            req = [x for x in ls if x.startswith('@@')]
            star = [('','.*')]*len(req)
            for req_order in itertools.permutations(req):
                for star_join in itertools.product(*star):
                    rls = list(x[0] + x[1] for x in zip(req_order, star_join))
                    rs = '.'.join(rls)
                    t1 = tags
                    t2 = tags + '.*'
                    if rs:
                        t1 += '.' + rs
                        t2 += '.' + rs
                    ct += '<cat-item tags="%s"/>' % t1
                    ct += '<cat-item tags="%s"/>' % t2
            ct += '</def-cat>\n'
            ret += ct
        return ret
    def get_rule(self):
        firstChunk = self.pattern[0].split('.')[0]
        if self.dep == 1:
            firstChunk = self.pattern[1].split('.')[0]
        name = '%s:' % self.ruleid
        for p in self.pattern:
            name += ' ' + p.split('.')[0]
        name += ' - %s > %s' % (self.head, self.dep)
        ret = '<rule firstChunk="%s" id="%s">\n  <pattern>\n' % (firstChunk, name)
        ret += '\n'.join('    <pattern-item n="%s_%s"/>' % (self.ruleid, i) for i in range(len(self.pattern)))
        ret += '\n  </pattern>\n  <action>\n'
        for i, p in enumerate(self.pattern):
            for tg in p.split('.'):
                if tg[0] != '!': continue
                ret += '    <let><var n="tag_param"/><lit-tag v="%s"/></let>\n' % tg[1:]
                ret += '    <call-macro n="negate"><with-param pos="%s"/></call-macro>\n' % (i+1)
        ret += '    <let><var n="head_tag"/><lit-tag v="@%s"/></let>\n' % self.rel
        ret += '    <let><var n="dep_tag"/><lit-tag v="%s"/></let>\n' % self.rel
        for i, p in enumerate(self.pattern):
            if self.dep == i+1: continue
            if not ((self.dep == 1 and i == 1) or (i == 0 and self.dep > 1)):
                ret += '    <out><b/></out>\n'
            if i + 1 == self.head:
                lr = 'left' if self.dep < self.head else 'right'
                ret += '    <call-macro n="out_dep_%s"><with-param pos="%s"/><with-param pos="%s"/></call-macro>\n' % (lr, self.head, self.dep)
            elif self.dep == 1 and i == 1:
                ret += '    <call-macro n="out_trace_left"><with-param pos="2"/><with-param pos="1"/></call-macro>\n'
            elif i + 2 == self.dep:
                ret += '    <call-macro n="out_trace_right"><with-param pos="%s"/><with-param pos="%s"/></call-macro>\n' % (i+1, self.dep)
            else:
                ret += '    <call-macro n="out_plain"><with-param pos="%s"/></call-macro>\n' % (i+1)
        ret += '  </action>\n</rule>\n'
        return ret

def parse_line(s, ruleid):
    ls = s.split()
    pat = list(itertools.takewhile(lambda x: x != ':', ls))
    act = list(itertools.dropwhile(lambda x: x != ':', ls))[1:]
    head = int(act[0])
    dep = int(act[2])
    if act[1] == '<':
        head, dep = dep, head
    rel = act[3]
    return Rule(ruleid, pat, head, dep, rel)

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as infile:
        rules = []
        for i, s_ in enumerate(infile):
            s = s_.strip()
            if s:
                rules.append(parse_line(s, i))
        with open(sys.argv[2], 'w') as outfile:
            outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            outfile.write('<transfer>\n<section-def-cats>\n')
            for r in rules:
                outfile.write(r.get_patterns())
            outfile.write('</section-def-cats>\n')
            outfile.write(common_content)
            outfile.write('<section-rules>\n')
            for r in rules:
                outfile.write(r.get_rule())
            outfile.write('</section-rules>\n</transfer>\n')
