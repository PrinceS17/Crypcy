import React from "react";
import {
  G2,
  Chart,
  Geom,
  Axis,
  Tooltip,
  Coord,
  Label,
  Legend,
  View,
  Guide,
  Shape,
  Facet,
  Util
} from "bizcharts";


import DataSet from "@antv/data-set";

class Areanull extends React.Component {
  render() {
    console.log("Arena");
    console.log(this.props.data);
    let sche = this.props.schema;
    if(!this.props.data)  return (<div></div>);
    let fie = [];
    fie.push(this.props.schema);
    if(this.props.schema =='price') fie.push('Price Prediction');
    var dv = new DataSet.View().source(this.props.data);
    dv.transform({
      type: "fold",
      fields: fie,
      key: "type",
      value: "value"
    });
    console.log(dv);
    const scale = {
      value: {
        alias: "The Share Price in Dollars",
        formatter: function(val) {
          if(sche==="price") return '$'+val;
          else if(sche==="volume") {
            val = val.toString();
            return '$' + val.substr(0, val.length-3) + 'M';
          }
          else return val;
        }
      },
      time: {
        range: [0, 1]
      }
    };
    return (
          <Chart
            data={dv}
            padding={"auto"}
            scale={scale}
            
            style={{zIndex: -2, marginBottom:'50px'}}
            height={400}
            width={1000}
          >
            <Tooltip crosshairs />
            
            <Axis name="value"/>
            <Axis name="time" visible={false}/> 
            <Legend />
            <Geom type="area" position="time*value" color="type" shape="smooth" />
            <Geom
              type="line"
              position="time*value"
              color="type"
              shape="smooth"
              size={2}
            />
          </Chart>
    );
  }
}

export default Areanull;