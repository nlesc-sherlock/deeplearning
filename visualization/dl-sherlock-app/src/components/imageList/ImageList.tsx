import * as React                   from 'react';
import { connect }                  from 'react-redux';
// import { AppRegistry, View, Image } from 'react-native';

import { Cell, Grid }       from 'react-mdl';
import { D3Chart }          from '../';
import { DLOutputJsonData } from '../../types';

import './ImageList.css';

export interface IImageList extends React.Props<any> {
    data : any;
}

export class UnconnectedImageList extends React.Component<IImageList, {}> {
    

    constructor() {
        super();        
    }

    static mapStateToProps(state: any) {
        return {
            data: state.imageChart.d3JSON
        };
    }

    static mapDispatchToProps() {
        return {};
    }

    render(): JSX.Element {
        const data = this.props.data;
        const elements: JSX.Element[] = [];
        

        if (data.images) {
            Object.keys(data.images).forEach((key: any) => {   
                const classes: JSX.Element[] = [];
                Object.keys(data.images[key].objects).forEach((classKey: any) => {
                    classes.push(
                        <Grid key= { key + classKey }>
                            <Cell col={6}>
                                {classKey}
                            </Cell>
                            <Cell col={6}>
                                {data.images[key].objects[classKey].probability}
                            </Cell>
                        </Grid>
                    );
                });

                elements.push(
                    <Grid className='mdl-cell mdl-cell--4-col' key={ key }>
                        <Cell col={6}>
                            { key }
                        </Cell>
                        <Cell col={6}>
                            { classes }
                        </Cell>
                        <Cell col={12}>                            
                            <D3Chart id={key} />:
                        </Cell>
                    </Grid>
                );
            });
        }

        return (
            <Grid>
                {elements}
            </Grid>
        );
    }
}

export const ImageList = connect(UnconnectedImageList.mapStateToProps,
                                 UnconnectedImageList.mapDispatchToProps)(UnconnectedImageList);
