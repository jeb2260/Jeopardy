import React,{Component} from "react"

class CorrectPerGame extends Component{
    constructor(props){
        super(props)
    }
    render(){
        return(
            <div>
                {"Correct Per Game"}<br />
                {this.props.correctPerGame.toFixed(2)}
            </div>
        )
    }
}

export default CorrectPerGame