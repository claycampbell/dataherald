import React, {
  ComponentType,
  FC,
  ReactNode,
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from 'react'
import { useRouter } from 'next/navigation'

interface AuthProviderProps {
  children: ReactNode
}

type WithAuthUser = (
  Component: ComponentType<AuthProviderProps>,
) => React.FC<AuthProviderProps>

const MockUser = {
  name: 'Mock User',
  email: 'mockuser@example.com',
  sub: 'mock|12345',
}
export const useUser = () => {
  return {
    user: {
      id: 'mock-user-123',
      name: 'Mock User',
      email: 'mockuser@example.com',
      organization_id: 'mock-org-456'
    },
    isLoading: false
  }
}
const withAuthUser: WithAuthUser = (Component) => {
  return function WithAuthUser(props: AuthProviderProps): JSX.Element {
    return <Component {...props} />
  }
}

interface AuthContextType {
  token: string | null
  user: typeof MockUser | null
  isAuthenticated: boolean
  fetchToken: () => Promise<void>
  login: () => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: FC<AuthProviderProps> = withAuthUser(
  ({ children }) => {
    const router = useRouter()
    const [token, setToken] = useState<string | null>(null)
    const [user, setUser] = useState<null | typeof MockUser>(null)
    const isAuthenticated = !!user

    const fetchToken = useCallback(async () => {
      // Simulate a token fetch
      const fakeToken = 'mocked-token-123'
      setToken(fakeToken)
    }, [])

    useEffect(() => {
      const isLoggedIn = localStorage.getItem('isLoggedIn')
      if (isLoggedIn) {
        const storedUser = localStorage.getItem('mockUser')
        setUser(storedUser ? JSON.parse(storedUser) : MockUser)
        fetchToken()
      } else {
        localStorage.setItem('isLoggedIn', 'true')
        localStorage.setItem('mockUser', JSON.stringify(MockUser))
        setUser(MockUser)
        fetchToken()
      }
    }, [fetchToken])

    const login = () => {
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('mockUser', JSON.stringify(MockUser))
      setUser(MockUser)
      fetchToken()
      router.push('/')
    }

    const logout = () => {
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('mockUser')
      setUser(null)
      router.push('/auth/error')
    }

    return (
      <AuthContext.Provider
        value={{ token, user, isAuthenticated, fetchToken, login, logout }}
      >
        {children}
      </AuthContext.Provider>
    )
  }
)

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
