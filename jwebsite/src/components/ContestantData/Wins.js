import React,{Component} from "react"

class Wins extends Component{
    constructor(props){
        super(props)
    }
    render(){
        return(
            <div>
                {"Wins"}<br />
                {this.props.wins}
            </div>
        )
    }
}

export default Wins