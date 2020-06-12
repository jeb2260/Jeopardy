import React,{Component} from "react"
import Accuracy from "./ContestantData/Accuracy.js"

class Category extends Component{
    constructor(props){
        super(props)
    }
    render(){
        var name = this.props.data[0];
        var data = this.props.data[1];
        var accuracy = ((data.CorrectAttempts)/(data.CorrectAttempts+data.IncorrectAttempts))*100;
        return(
            <div>
                {"Title: " +name}<br />
                   {"Games Appeared: "+ data.GamesAppeared} <br />
                   {"Contestant Accuracy"}
                   <Accuracy numberCorrect={data.CorrectAttempts} numberIncorrect={data.IncorrectAttempts}
                   overallAccuracy = {accuracy}/>
                   {"Daily Double Count: "+data.DailyDoubleCount} <br />
                   {"Final Jeopardy Count: "+data.FinalJeopardyCount} <br />
                   {"Tiebreak Count: "+data.TiebreakerCount} <br />
                   {"Unselected Clues: "+data.UnselectedClues} <br />
                   {"Average Pick Order: "+data.AveragePickOrder} 
            </div>
        )
    }
}

export default Category