var assert = chai.assert

  describe('#BarChartTests', function () {
    describe('#Content', function () {
      it(`柱状图需要有一个标题(使用什么元素来表示自定)，这个元素的id属性需要为"title"`, function () {
        assert.isNotNull(
         document.getElementById('title'),
          '无法匹配到id="title"的元素 '
        );
      });

      it(`柱状图需要有一个<g>元素表示的x轴，并且这个元素的id="x-axis"`, function () {
        assert.isAbove(
          document.querySelectorAll('g#x-axis').length,
          0,
          '无法匹配到id="x-axis"的<g>元素'
        );
      });

      it(`柱状图需要有一个<g>元素表示的y轴，并且这个元素的id="y-axis"`, function () {
        assert.isAbove(
          document.querySelectorAll('g#y-axis').length,
          0,
          '无法匹配到id="y-axis"的<g>元素'
        );
      });

      it(`两个坐标轴上都应该包含多个刻度标签，每个标签具有class="tick"属性`, function () {
        assert.isAbove(
          $('#x-axis .tick').length,
          1,
          'x轴上的刻度标签不足'
        );
        assert.isAbove(
          $('#y-axis .tick').length,
          1,
          'y轴上的刻度标签不足'
        );
      });

      it(`每个数据点都应该有一个具有class="bar"属性的<rect>元素来展示数据`, function () {
        assert.isAbove(
          document.querySelectorAll('rect.bar').length,
          0,
          '没有匹配到class="bar"的<rect>元素'
        );
        assert.equal(
          document.querySelectorAll('rect.bar').length,
          275,
          '柱形的数目和数据的数目不相等'
        );
      });

      it('每一个柱形都需要具有包含日期的data-date属性以及包含 GDP 值的data-gdp属性',function(){
        let bars = document.querySelectorAll('rect.bar')
        assert.isAtLeast(bars.length,1,'没有匹配到class="bar"的<rect>元素')
        bars.forEach(function(bar){
          assert.isNotNull(bar.getAttribute('data-date'),'柱形没有data-date属性')
          assert.isNotNull(bar.getAttribute('data-gdp'),'柱形没有data-gdp属性')
        })
      })

      it('柱状图的每一个元素中的"data-date"属性的值应该按照数据原始的顺序和数据值一一对应',function(done){
  
        $.getJSON('https://gist.githubusercontent.com/935462955/0de28ba6f0ff3d309f60a6eb58cbdcca/raw/e231d4b887e14efd6203fd6d0c08903392905539/GDP.json',
        function(res){
          try{
          let bars = document.querySelectorAll('rect.bar')
          assert.isAtLeast(bars.length,1,'找不到包含类名为"bar"的<rect>元素')
          bars.forEach(function(bar,i){
            let date = bar.getAttribute('data-date')
            assert.equal(date,res.data[i][0],'柱形的日期数据和原始数据顺序不一致')
          })
          done()
          }
          catch(e){
            done(e)
          }
        })
      }).timeout(10000)

       it(`柱状图的每一个元素中的"data-gdp"属性的值应该按照数据原始的顺序和数据值一一对应`, function (done) {
   
        $.getJSON('https://gist.githubusercontent.com/935462955/0de28ba6f0ff3d309f60a6eb58cbdcca/raw/e231d4b887e14efd6203fd6d0c08903392905539/GDP.json',
          function (res) {
            try {
              const bars = document.querySelectorAll('rect.bar');
              assert.isAtLeast(
                bars.length,
                1,
                '找不到包含类名为"bar"的<rect>元素'
              );
              bars.forEach(function (bar, i) {
                let gdp = bar.getAttribute('data-gdp');
                assert.equal(
                  gdp,
                  res.data[i][1],
                  '柱形的gdp数据和原始数据顺序不一致'
                );
              });
              done();
            } catch (e) {
              done(e);
            }
          }
        );
      });
      it(`每一个柱形的高度需要按比例和gdp对应`, function () {
        let bars = document.querySelectorAll('rect.bar');
        let firstRatio =
          parseFloat(bars[0].getAttribute('data-gdp')) /
          parseFloat(bars[0].getAttribute('height'));
        //计算第一个柱形高度和gdp的比例
        /* 其实这一个测试用例就足够验证柱形图是否合规了，但是为了方便学生细化任务所以首先验证了data-gdp和data-date属性 */
        bars.forEach(function (bar) {
          let dataValue = bar.getAttribute('data-gdp');
          let barHeight = bar.getAttribute('height');
          let ratio = parseFloat(dataValue) / parseFloat(barHeight);
          assert.equal(
            firstRatio.toFixed(3),//小数点后三位
            ratio.toFixed(3),
            '柱形的高度需要和数据中的gdp按比例对应'
          );
        });
      });

      it(`每个柱形的位置都应该按照 data-date 属性的值和 x 坐标轴上的刻度对齐`, function () {
        const axis = document.querySelector('#x-axis');
        const coordAttr = 'x';
        const barsCollection = document.querySelectorAll('.bar');
        const ticksCollection = axis.querySelectorAll('.tick');
        const shapeAttr = 'data-date';
        // options are 'minute', 'month', 'thousand', and 'year'
        const dataType = 'year';
        // what vertex of shape to measure against the axis
        // options are 'topLeft' and 'center'
        const shapeAlign = 'topLeft';

        assert.isAbove(
          barsCollection.length,
          0,
          '没有检测到包含类名为“bar”的<rect>元素'
        );

        assert.isTrue(
          areShapesAlignedWithTicks(
            barsCollection,
            ticksCollection,
            coordAttr,
            shapeAttr,
            dataType,
            shapeAlign
          ),
          "柱形的x值和x轴刻度没对齐"
        );
      });

      it(`每个柱形的位置都应该按照 data-gdp 属性的值和 y 坐标轴上的刻度对齐`, function () {
        
        const barsCollection = document.querySelectorAll('.bar')
        const ticksCollection = document.querySelector('#y-axis').querySelectorAll('.tick')
        const coordAttr = 'y'
        const shapeAttr = 'data-gdp'
        const dataType = 'thousand'
        const shapeAlign = 'topleft'

        assert.isAbove(
          barsCollection.length,
          0,
          '没有检测到包含类名为“bar”的<rect>元素'
        );

        assert.isTrue(
          areShapesAlignedWithTicks(
            barsCollection,
            ticksCollection,
            coordAttr,
            shapeAttr,
            dataType,
            shapeAlign
          ),
          "柱形的y值和x轴刻度没对齐"
        );
      });
    });
    })
