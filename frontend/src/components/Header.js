import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Navbar, Nav, Container, Row, NavDropdown } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import SearchBox from './SearchBox'
import { logout } from '../actions/userAction'
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import LogoutIcon from '@mui/icons-material/Logout';
import LoginIcon from '@mui/icons-material/Login';
import MenuBookIcon from '@mui/icons-material/MenuBook';
function Header() {

    const userLogin = useSelector(state => state.userLogin)
    const { userInfo } = userLogin

    const dispatch = useDispatch()

    const logoutHandler = () => {
        dispatch(logout())
    }

    return (
            <Box sx={{ flexGrow: 1 }}>
                <AppBar position="static">
                    <Toolbar>
                    <LinkContainer to='/'>
                        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            <MenuBookIcon/>Book Mart
                        </Typography>
                    </LinkContainer>
                    <LinkContainer to='/cart'>
                        <Button color="inherit"><ShoppingCartIcon/>Cart</Button>
                    </LinkContainer>

                    {userInfo ? (
                        <div>
                            <LinkContainer to='/profile'>
                                <Button color="inherit"><AccountCircleIcon/> Profile</Button>
                            </LinkContainer>
                            
                            <Button color="inherit"onClick={logoutHandler}><LogoutIcon/>Logout</Button>
                            
                        </div>

                        ) : (
                        <LinkContainer to='/login'>
                            <Button color="inherit"><LoginIcon/>Login</Button>
                        </LinkContainer>
                        )}
                    {userInfo && userInfo.is_admin && (
                        <NavDropdown title='Admin' id='adminmenue'>
                        <LinkContainer to='/admin/userlist'>
                            <NavDropdown.Item>Users</NavDropdown.Item>
                        </LinkContainer>

                        <LinkContainer to='/admin/productlist'>
                            <NavDropdown.Item>Products</NavDropdown.Item>
                        </LinkContainer>

                        <LinkContainer to='/admin/orderlist'>
                            <NavDropdown.Item>Orders</NavDropdown.Item>
                        </LinkContainer>

                    </NavDropdown>
                    )}
                    
                    
                    </Toolbar>
                </AppBar>
                </Box>
    )
}

export default Header
