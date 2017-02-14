import { Dispatch }                             from 'redux';

import { exampleAction }                        from '../';
import { exampleThunkAction }                   from '../';
import { GenericAction }                        from '../../types';

export const exampleThunk = (imageSrc: string) => {
    return (dispatch: Dispatch<GenericAction>) => {
        const handleTheStatus = (response: Response) => {
            if (response.ok) {
                return response.url;
            } else {
                throw new Error('Error when trying to get image. ' +
                    'status text: \"' + response.statusText + '".');
            }
        };

        const handleAnyErrors = (err : Error) => {
            throw new Error('Errors occured. ' + err.message + err.stack);
        };

        const handleTheData = (result: any) => {

            dispatch(exampleAction(result));
        };

        //Here we can handle any loading bars or something
        dispatch(exampleThunkAction(imageSrc));

        const url: string = imageSrc;

        fetch(url, {method: 'get'})
          .then(handleTheStatus)
          .then(handleTheData)
          .catch(handleAnyErrors);
    };
};
