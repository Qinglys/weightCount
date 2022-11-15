function gen_charts(chart_own, weight_data, chart_date){

  only_number_weight = new Set(weight_data)
  only_number_weight.delete('_')
  option = {
      legend: {
        data: [chart_own]
      },
      xAxis: {
        type: 'category',
        name: '日期',
        data: chart_date,
      
      },
      yAxis: {
        type: 'value',
        name: '体重/KG',
        min: Math.round(Math.min.apply(null,Array.from(only_number_weight)) - 1),
        max: Math.round(Math.max.apply(null,Array.from(only_number_weight)) + 1)
      },
      series: [
        {
          name: chart_own,
          data: weight_data,
          type: 'line',
          // smooth: true,
          markPoint: {
          data: [
            { type: 'max', name: 'Max' },
            { type: 'min', name: 'Min' }
          ]
        },
        }
      ]
  };
  return option
}

function get_weight_data(){
  const xhr = new XMLHttpRequest();
  xhr.open('GET', window.location.href+'get_weight', false);
  xhr.send();
  xhr.onreadystatechange=function(){
    if (xhr.readyState==4 && xhr.status==200){
      console.log(xhr.response)
      return xhr.response
    }
    else if(xhr.readyState==4 && xhr.status!= 200){
      console.log('1111 ')
      return {}
    }
  }
}

function add_weight_data(data){
  document.activeElement.blur()
  document.body.scrollTop = document.documentElement.scrollTop = 0;
  const xhr = new XMLHttpRequest();
  xhr.open('POST', window.location.href+'add_weight');
  xhr.setRequestHeader('content-type', 'application/json')
  xhr.send(JSON.stringify(data));
  xhr.onreadystatechange=function(){
    // 成功
    if (xhr.readyState==4 && xhr.status==200){
      //console.log(xhr.response)
      // 弹窗
      layui.use('layer', function() { //独立版的layer无需执行这一句
        var layer = layui.layer;
        function func_msg() {
            layer.alert(JSON.parse(xhr.responseText)['msg'], {
                icon: 1,
                skin: 'layer-ext-moon',
              },
              function(){
                location.reload()
              });
        }
        func_msg();
      })
      return false
    }
    // 失败
    else if(xhr.readyState==4 && xhr.status!= 200){
      // 弹窗
      layui.use('layer', function() { //独立版的layer无需执行这一句
        var layer = layui.layer;
        function func_msg() {
            layer.alert(JSON.parse(xhr.responseText)['msg']);
        }
        func_msg();
      })
      return false
    }
  }
}