import sys
import profile as profiler
import pstats
#import cProfile

sys.path.insert(0, '/Users/chrism/projects/meld/z310/lib/python')
from zope.pagetemplate.pagetemplate import PageTemplate

class mypt(PageTemplate):
    def pt_getContext(self, args=(), options={}, **kw):
        rval = PageTemplate.pt_getContext(self, args=args)
        options.update(rval)
        return options

template = """<html xmlns:tal="http://xml.zope.org/namespaces/tal">
  <head>
    <title>This is the title</title>
    <div>This is the head slot</div>
  </head>
  <body>
   <div>
     <form action="." method="POST">
     <table border="0">
       <tbody>
         <tr tal:repeat="itemz values" class="foo">
         <td tal:content="python: itemz[0]">Name</td>
         <td tal:content="python: itemz[1]">Description</td>
         </tr>
       </tbody>
     </table>
     </form>
    </div>
  </body>
</html>"""

values = []
for thing in range(0, 20):
    values.append((str(thing), str(thing)))

def test(pt):
    foo = pt(values=values)

def profile(num):
    profiler.run("[test(pt) for x in range(0,20)]", 'logfile_zpt.dat')
    stats = pstats.Stats('logfile_zpt.dat')
    stats.strip_dirs()
    stats.sort_stats('cumulative', 'calls')
    #stats.sort_stats('calls')
    stats.print_stats(num)
    
if __name__ == '__main__':
    pt = mypt()
    pt.write(template)
    test(pt)
    profile(30)
    import timeit
    t = timeit.Timer("test(pt)", "from __main__ import test, pt")
    print "300 runs", t.timeit(300)


    