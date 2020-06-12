import React,{Component} from "react"
import CanvasJSReact from '../../assets/canvasjs.react';
import "../../App.css"
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

class Accuracy extends Component{
    constructor(props){
        super(props)
    }
    render(){
		var correctAccuracy = ((this.props.overallAccuracy).toFixed(2)).toString()
		var incorrectAccuracy = ((100-this.props.overallAccuracy).toFixed(2)).toString()
        var options = { 
			title: {
				text: this.props.title
			},
			animationEnabled: false,
			animationEnabled: true,
			animationDuration: 500,
			backgroundColor: "#F0F8FF",
			height: 260,
			data: [{
				type: "pie",
				startAngle: 300,
				toolTipContent: "{accuracy}%",
				indexLabelFontSize: 16,
				indexLabel: "{label}:{y}",
				dataPoints: [
					{ y: this.props.numberCorrect, label: "Correct", accuracy: correctAccuracy },
					{ y: this.props.numberIncorrect, label: "Incorrect", accuracy: incorrectAccuracy},
				]
			}]
		}

        return (
            <CanvasJSChart className="chart" containerProps = {{ width: "50%" }} options = {options}/>
        )
    }
}

export default Accuracy