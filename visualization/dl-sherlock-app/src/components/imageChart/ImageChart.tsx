import * as React                   from 'react';
import { connect }                  from 'react-redux';

import Faux from 'react-faux-dom';
import * as d3 from 'd3';

import { charting } from './charting';

import './ImageChart.css';

export interface IImageChart {
    d3JSON : any;
}

export interface IExtraProps {
    id: any;
}


export class UnconnectedImageChart extends React.Component<IImageChart & IExtraProps, { }> {
    private chart : charting.Chart;
    
    constructor() {
        super();
        // this.canvasRefHandler = this.canvasRefHandler.bind(this);
    }

    static mapStateToProps(state: any, myProps: IExtraProps) {
        return {
            id: myProps.id,
            d3JSON: state.imageChart.d3JSON
        };
    }

    static mapDispatchToProps() {
        return {};
    }

    render(): JSX.Element {
        var el = Faux.createElement('div');

        // Change stuff using actual DOM functions.
        // Even perform CSS selections!
        el.style.setProperty('color', 'red');
        el.setAttribute('class', 'box');

        const jsx : JSX.Element = el.toReact();

        // Render it to React elements.
        return (jsx);//(el.toReact());
    }

    // componentWillMount() {
    //     const faux = Faux.connectFauxDOM('div', 'chart')
    //     d3.performSomeAnimation(faux)
    //     Faux.animateFauxDOM(3500) // duration + margin
    // }

    // componentDidMount() {
    //     this.chart = new charting.Chart('#test');
    //     this.chart.draw();   
    // }

    // private canvasRefHandler(ref: Element) {
    //     ref.id = this.props.id;
    // }
}

// Export just the connected component
export const ImageChart = connect(UnconnectedImageChart.mapStateToProps,
                                  UnconnectedImageChart.mapDispatchToProps)(UnconnectedImageChart);
