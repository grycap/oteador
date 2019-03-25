 

API_url = "https://g14e5vv1h6.execute-api.us-east-1.amazonaws.com/dev/"
type = "services"

//import Table from './Table'
//import './css/_variables.scss';

window.select = new Vue({
    el: "#select_option",
    data: {
        selected: '',
        options: [
            { text: 'Buckets', value: 1 },
            { text: 'Instances EC2', value: 2 },
            { text: 'Instances RDS', value: 3 },
            { text: 'Elastic Load Balancing', value: 4 },
            { text: 'Auto Scalling Groups', value: 5 },
            { text: 'Elastic IP not connected', value: 6 }
        ],
        select : function () {
            console.log(this.selected.text)
            switch (this.selected.value) {
                case 1:
                    select_service('AllBuckets')
                    break;
                case 2:
                    select_service('AllInstancesEC2')
                    break;
                case 3:
                    select_service('AllInstancesRDS')
                    break;
                case 4:
                    select_service('ElasticLoadBalancing')
                    break;
                case 5:
                    select_service('AutoScallingGroups')
                    break;
                case 6:
                    select_service('ElasticIP')    
                    break;
                default:
                // code block
            } 
        }
    }
})

var table = new Vue({
    el: '#tabla',
    data: {
      ascending: false,
      sortColumn: '',
      cols: [],
      rows : []
    },
    methods: {
      "sortTable": function sortTable(col) {
        if (this.sortColumn === col) {
          this.ascending = !this.ascending;
        } else {
          this.ascending = true;
          this.sortColumn = col;
        }
  
        var ascending = this.ascending;
  
        this.rows.sort(function(a, b) {
          if (a[col] > b[col]) {
            return ascending ? 1 : -1
          } else if (a[col] < b[col]) {
            return ascending ? -1 : 1
          }
          return 0;
        })
      },
      addItem(item) {
        this.rows.push(item);
      },
      removeItems() {
        this.rows = [];
        this.cols = [];
      }

    },
    computed: {
      "columns": function columns() {
        if (this.rows.length == 0) {
          return [];
        }
        return Object.keys(this.rows[0])
      }
    }
  });

function select_service (service) {
    url = API_url + type + "/" + service;
    console.log(url)
    jQuery.ajax({
        url: url,
        type: 'GET',
        contentType: "application/json",
        success: function (data) {
            console.log("Success")
            console.log(data)
            table.removeItems();
            for (i = 0; i < data.body.response.length; i++) { 
              table.addItem(data.body.response[i]);
            }
            return data.body.response

        },
        error: function (jqXHR, textStatus, errorThrown) {
            var code = jqXHR.status
            console.log(("error " + code));
            console.log(jqXHR.responseText)
            console.log(jqXHR)
        },
    })
}