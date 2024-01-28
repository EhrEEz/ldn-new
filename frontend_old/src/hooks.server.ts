import { getCurrentUser } from '$lib/utils/requestUtils';
import { variables } from '$lib/utils/constants';
import type { Handle } from '@sveltejs/kit';
import {error} from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
    const session = event.cookies.get('refreshToken')
  
    if (!session) {
      return await resolve(event)
    }
  
    const [response, errs] = await getCurrentUser(fetch,`${variables.BASE_API_URI}/token/refresh/`, `${variables.BASE_API_URI}/user/`, session )
  
    if(errs.length > 0 ){
        throw error(500, "Server Error");
    }
    if (response) {
      event.locals.user = response;
    }
  
    return await resolve(event)
  }