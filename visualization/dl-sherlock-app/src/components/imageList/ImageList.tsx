import * as React                   from 'react';
import { connect }                  from 'react-redux';
// import { AppRegistry, View, Image } from 'react-native';

import { D3Chart }          from '../';
import { Cell, Grid }       from 'react-mdl';

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
                const name = data.images[key].name;
                const classes: JSX.Element[] = [];

                Object.keys(data.images[key].objects).forEach((classKey: any) => {
                    const details: JSX.Element[] = [];
                    if (data.images[key].objects[classKey].detail) {
                        Object.keys(data.images[key].objects[classKey].detail.classification).forEach((detailKey: any) => {
                            Object.keys(data.images[key].objects[classKey].detail.classification[detailKey].classes).forEach((detailClassKey: any) => {
                                details.push(
                                    <Grid key= { key * 4568 + classKey * 488 + detailKey * 47 + detailClassKey}>
                                        <Cell col={ 6 }>
                                            {data.images[key].objects[classKey].detail.classification[detailKey].classes[detailClassKey].name}
                                        </Cell>
                                        <Cell col={ 6 }>
                                            {data.images[key].objects[classKey].detail.classification[detailKey].classes[detailClassKey].probability}
                                        </Cell>
                                    </Grid>
                                );
                            });
                        });
                    }

                    if (data.images[key].objects[classKey].classification) {
                        Object.keys(data.images[key].objects[classKey].classification).forEach((detailKey: any) => {
                            Object.keys(data.images[key].objects[classKey].classification[detailKey].classes).forEach((detailClassKey: any) => {
                                details.push(
                                    <Grid key= { key * 4568 + classKey * 488 + detailKey * 47 + detailClassKey}>
                                        <Cell col={ 6 }>
                                            <span className={'redText'}></span>
                                            {data.images[key].objects[classKey].classification[detailKey].classes[detailClassKey].name}
                                        </Cell>
                                        <Cell col={ 6 }>
                                            <span className={'redText'}></span>
                                            {data.images[key].objects[classKey].classification[detailKey].classes[detailClassKey].probability}
                                        </Cell>
                                    </Grid>
                                );
                            });
                        });
                    }

                    const className = data.images[key].objects[classKey].className;
                    classes.push(
                        <Grid key= { key * 4568 + classKey }>
                            <Cell col={ 2 }>
                                <span className={'redText'}>{ className }</span>
                            </Cell>
                            <Cell col={ 2 }>
                                <span className={'redText'}>{ data.images[key].objects[classKey].probability }</span>
                            </Cell>
                            <Cell col={ 8 }>
                                <span className={'redText'}>{ details }</span>
                            </Cell>
                        </Grid>
                    );
                });

                elements.push(
                    <Grid className={'mdl-cell mdl-cell--12-col category'} key={ key }>                        
                        <Cell col={ 8 }>
                            <span className={'redText'}>{name}</span>
                            <D3Chart id={ key } />:
                        </Cell>
                        <Cell col={ 4 }>
                            { classes }
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
