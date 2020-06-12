import React,{Component} from "react"
import Appearances from "./ContestantData/Appearances"
import Wins from "./ContestantData/Wins"
import CorrectPerGame from "./ContestantData/CorrectPerGame"
import Accuracy from "./ContestantData/Accuracy"
import "../App.css"

class Contestant extends Component{
    constructor(props){
        super(props)
    }
    render(){
        var name = this.props.data[0];
        var data = this.props.data[1];
        let fjText = null
        let fj = null
        if (data.FJCorrect+data.FJIncorrect>0){
            fjText = "FJ! Accuracy";
            fj = <Accuracy title = {fjText} numberCorrect={data.FJCorrect} numberIncorrect={data.FJIncorrect}
            overallAccuracy = {data.FJAccuracy}/>
        }
        let tiebreak = null
        let tiebreakText = null 
        if (data.TiebreakCorrect+data.TiebreakIncorrect>0){
            tiebreakText = "Tiebreak Accuracy"
            tiebreak = <Accuracy title = {tiebreakText} numberCorrect={data.TiebreakCorrect} 
            numberIncorrect={data.TiebreakIncorrect} overallAccuracy = {data.TiebreakAccuracy} />
        }
        return(
            <div className= "chart">
                {name}
                <Appearances firstAppearance={data.firstAppearance} 
                            lastAppearance={data.lastAppearance} />
                <Wins wins={data.wins} />
                <CorrectPerGame correctPerGame={data.CorrectPerGame} />
                
                <Accuracy title = "Overall Accuracy" numberCorrect={data.numberCorrect} numberIncorrect={data.numberIncorrect}
                overallAccuracy = {data.overallAccuracy}/>
                
                <Accuracy title = "J! Accuracy" numberCorrect={data.JCorrect} numberIncorrect={data.JIncorrect}
                overallAccuracy = {data.JAccuracy}/>
                
                <Accuracy title = "DJ! Accuracy" numberCorrect={data.DJCorrect} numberIncorrect={data.DJIncorrect}
                overallAccuracy = {data.DJAccuracy}/>
                {fj}
                {tiebreak}
            </div>
        )
    }
}

export default Contestant