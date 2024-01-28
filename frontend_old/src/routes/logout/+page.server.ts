import { redirect } from '@sveltejs/kit'
import type { Actions, PageServerLoad } from './$types'
import { logOutUser } from '$lib/utils/requestUtils'

export const load: PageServerLoad = async () => {
  // we only use this endpoint for the api
  // and don't need to see the page
  throw redirect(302, '/')
}

export const actions: Actions = {
  async default({ cookies }) {
    await logOutUser(cookies.get('refreshToken'))
    cookies.delete('refreshToken');


    // redirect the user
    throw redirect(302, '/login')
  },
}