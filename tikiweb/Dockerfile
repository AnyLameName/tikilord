FROM node
LABEL maintainer="jay.gagnon@gmail.com"
WORKDIR /code/
COPY package.json package-lock.json /code/
RUN npm install --no-audit
COPY src /code/src
COPY public /code/public
EXPOSE 3000
CMD ["npm", "start"]
