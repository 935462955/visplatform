         const mark_todo = '- [ ] '
         const mark_finish = '- [x] '
         function runtest(goal){
         let code = window.parent.editor.getValue()//用户提交的代码
         let global = this.contentWindow
         window.parent.toIframe()
             //  console.log(width)
         let all_pass = true
         let output_result = ``
         goal.map((test,index)=>{
           try {
             //  console.log(eval(test['teststring']))
               if (eval(test['teststring'])) {
                   output_result = output_result + mark_finish + '~~' + test['text'] + '~~  \n'
               } else {
                   output_result= output_result + mark_todo + test['text'] + '  \n'
                   all_pass = false
               }
           }
            catch{
                output_result = output_result + mark_todo + test['text'] + '  \n'
                all_pass = false
            }
         })
        window.parent.document.querySelector(
        "#div_test"
         ).innerHTML = window.parent.marked(output_result)
        if(all_pass)
        {
            window.parent.document.querySelector('#button_show_model').click()
        }

      }
