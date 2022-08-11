import React from 'react'

import Rating from './Rating'
import { Link } from 'react-router-dom';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';

function Product({ product }) {
  return (

    <Card className='my-3 p-3 rounded'>
        <Link to={`/product/${product._id}`}>

        <CardActionArea>
            <CardMedia
                component="img"
                image={product.image}
                alt="green iguana"
            />
            <CardContent>
                <Typography variant="h6">
                    {product.name}
                </Typography>
    
            </CardContent>
        </CardActionArea>


        </Link>
        
  </Card>
    
  )
}

export default Product