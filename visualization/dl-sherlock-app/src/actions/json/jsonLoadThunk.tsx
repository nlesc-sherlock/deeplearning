import * as d3 from 'd3';
import { Dispatch }                             from 'redux';

import { jsonLoadAction }                       from '../';
import { GenericAction }                        from '../../types';
import { DLOutputJsonData }                     from '../../types';

export const jsonLoadThunk = (jsonpath: string) => {
    return (dispatch: Dispatch<GenericAction>) => {
        const url: string = jsonpath;
        
        const d3JSONRequest = d3.json(url, (error: any, data: DLOutputJsonData) => {
            if (error) {
                throw error;
            }
            dispatch(jsonLoadAction(data));
        });

        d3JSONRequest.get();
    };
};
