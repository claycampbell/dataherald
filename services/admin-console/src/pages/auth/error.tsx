import BackgroundPageLayout from '@/components/layout/background-page-layout'
import { Button } from '@/components/ui/button'
import { AUTH } from '@/config'
import { MailWarning } from 'lucide-react'
import { GetServerSideProps } from 'next'
import Head from 'next/head'
import { useRouter } from 'next/router'
import { FC, useState } from 'react'

enum ERROR_CODES {
  EMAIL_NOT_VERIFIED = 'Email Not Verified',
}

/**
 * Auth0 wraps several errors like unverified emails into a CallbackError
 * We implemented this to catch different callback scenarios and catch the errors for UX
 * @param errorDescription
 * @returns
 */
const getErrorCause = (errorDescription: string): string => {
  const error = (errorDescription.match(/---(.*?)\)/) || '')[1]
  switch (error) {
    case ERROR_CODES.EMAIL_NOT_VERIFIED:
      return 'Verify your email address'
    default:
      return "We couldn't verify your identity"
  }
}

export const getServerSideProps: GetServerSideProps = async (context) => {
  const { message = '' } = context.query
  const errorDescription = message as string
  const isEmailNotVerified = errorDescription?.includes(
    ERROR_CODES.EMAIL_NOT_VERIFIED,
  )
  const errorCause = getErrorCause(errorDescription)

  const logoutUrl = `${AUTH.domain}/v2/logout?client_id=${AUTH.cliendId}&returnTo=${AUTH.hostname}`

  return {
    props: {
      errorCause,
      errorDescription,
      isEmailNotVerified,
      logoutUrl,
    },
  }
}

const AuthErrorPage: FC = () => {
  const router = useRouter()

  // Automatically redirect to homepage
  useEffect(() => {
    router.push('/')
  }, [router])

  return (
    <BackgroundPageLayout>
      <Head>
        <title>Redirecting - Dataherald API</title>
      </Head>
      <div className="bg-white shadow-lg w-full max-w-none h-screen rounded-none sm:rounded-2xl sm:h-fit p-8 sm:max-w-lg">
        <h1 className="text-xl font-bold mb-4 text-secondary-dark">
          Redirecting...
        </h1>
        <p className="text-slate-800 break-words">
          You are being redirected. If nothing happens, click{' '}
          <a
            className="text-primary font-semibold hover:underline cursor-pointer"
            onClick={() => router.push('/')}
          >
            here
          </a>
          .
        </p>
      </div>
    </BackgroundPageLayout>
  )
}

export default AuthErrorPage
